from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import get_db
from app.db.base import Base
from app.models.transaction import Transaction
from app.models.category import Category
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Create a new database session for a test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def test_client(db_session):
    """
    Create a test client that uses the test database.
    """
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    del app.dependency_overrides[get_db]

def test_read_transactions(test_client, db_session):
    """
    Integration test for the read_transactions API endpoint.
    """
    category = Category(name="Test Category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    transaction1 = Transaction(description="Test 1", amount=100, type="debit", category_id=category.id, user_id=1)
    transaction2 = Transaction(description="Test 2", amount=200, type="credit", category_id=category.id, user_id=1)
    db_session.add(transaction1)
    db_session.add(transaction2)
    db_session.commit()
    db_session.refresh(transaction1)
    db_session.refresh(transaction2)

    response = test_client.get("/api/v1/transactions/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["description"] == "Test 1"
    assert data[1]["description"] == "Test 2"
