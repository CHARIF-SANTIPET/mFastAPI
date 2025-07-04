from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# Step 1: Create a SQLAlchemy engine
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")  # SQLite database         

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})  # For SQLite

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Depaendency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# เทียบ class กับ ORM หากมีตัวไหนแตกต่างกันหรือหายไปก็ให้เพิ่มเข้าไป เพื่อทำให้ class ที่อยู่ใน code กับ class ของ database มีความสอดคล้องกัน
# Create database
Base.metadata.create_all(bind=engine)
