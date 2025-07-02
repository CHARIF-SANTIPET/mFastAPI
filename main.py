from fastapi import FastAPI, Request
from pydantic import BaseModel
# from typing import Union

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/items")
def create_item(item: Item):
    return {"requested_item": item}