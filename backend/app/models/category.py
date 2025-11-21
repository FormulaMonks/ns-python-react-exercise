from sqlalchemy import Column, Integer, String
from app.db.base import Base
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    transactions = relationship("Transaction", back_populates="category_rel")
