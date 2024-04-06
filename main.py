from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
import requests
from dotenv import load_dotenv
import os

from scripts.brave import search as brave_search
from brave_index import check_for_updates

# Load environment variables
load_dotenv()

# Environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")

# Environment variable for database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/dbname")

Base = declarative_base()

# Example model
class SearchResult(Base):
    __tablename__ = "search_results"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())

# Create engine and session

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup():
    # Ensure the database is connected; this can be expanded to include any startup tasks
    pass

@app.on_event("shutdown")
async def shutdown():
    # Handle any cleanup or shutdown tasks
    pass

@app.get("/index_updated")
async def index_updated(db: Session = Depends(get_db)):
    updated, urls = check_for_updates(db)
    return {"updated": updated, "urls": urls}
