from http.client import HTTPException
from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session

from .database import Base ,engine, get_db  # Import the database setup and session dependency

from.models import Item  # Import the ORM model

from .schema import ItemCreate, ItemResponse  # Import the Pydantic models

app = FastAPI()

@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.model_dump())  # Convert Pydantic model to dict to ORM model
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item  # Return the ORM model, which will be converted to Pydantic model by FastAPI


@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()  # Query the database for the item
    return db_item

@app.get("/items", response_model=list[ItemResponse])
def read_item(db: Session = Depends(get_db)):
    db_item = db.query(Item).all()  # Query the database for the item
    return db_item

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first() 
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in item.model_dump().items():
        setattr(db_item, key, value) 
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"detail": "Item deleted successfully"}


