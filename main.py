from fastapi import FastAPI, Depends
from pydantic import BaseModel

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Step 1: Create a SQLAlchemy engine 
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"  
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})  # For SQLite

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Step 2: ORM Class
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer)

# เทียบ class กับ ORM หากมีตัวไหนแตกต่างกันหรือหายไปก็ให้เพิ่มเข้าไป เพื่อทำให้ class ที่อยู่ใน code กับ class ของ database มีความสอดคล้องกัน
# Create database
Base.metadata.create_all(bind=engine)

#  Step 3: Pydantic Model
#  1 - Base
class ItemBase(BaseModel):
    title: str
    description: str 
    price: float

#  2 - Request    ตัวขาเข้า - รับข้อมูล ไปใช้กับ ORM | ตัวขาออก - ส่งข้อมูล แปลง ORM เป็น JSON ส่งออกไปยัง client
class ItemCreate(ItemBase):
    # ภายในจะมี logic การแปลงข้อมูลจาก Pydantic Model ไปเป็น ORM Model
    # เช่นการลดราคา มีการคำนวณราคาใหม่ก่อนไปใช้กับ ORM
    pass #ยังไม่มี logic อะไรแค่รับมาแล้วส่งไป

# 3 - Response   ตัวขาออก - ส่งข้อมูล แปลง ORM เป็น JSON ส่งออกไปยัง client
class ItemResponse(ItemBase):
    id: int  # ต้องมี id ด้วยเพราะ ORM Model มี id
    class Config:           # ตัว pydantic มีตัวช่วยในการแปลงข้อมูลจาก ORM Model ไปเป็น Pydentic Model 
        from_attributes = True     # (ซึ่งก็เป็น JSON ในการส่งไปยัง client แหละ) ซึ่งต้องกำหนด orm_mode เป็น True เพื่อให้ Pydantic รู้ว่าเราจะใช้ ORM Model


# Depaendency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.model_dump())  # Convert Pydantic model to dict to ORM model
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item  # Return the ORM model, which will be converted to Pydantic model by FastAPI


# @app.get("/")
# def hello_world():
#     return {"message": "Hello, World!"}

# @app.get("/items", response_model=ItemResponse)
# def read_item(db: Session = Depends(get_db)):
#     list[ItemResponse]: items = get_db  # Call the function to get all items
#     return  Session.query(Item).all()  # Get all items from the database

