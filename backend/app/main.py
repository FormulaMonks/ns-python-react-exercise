from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import get_db
from app.api.v1.endpoints import transactions

app = FastAPI(
    title="FinTech Transaction Dashboard API",
    description="API for managing and visualizing financial transactions.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router, prefix="/api/v1", tags=["transactions"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FinTech Transaction Dashboard API!"}
