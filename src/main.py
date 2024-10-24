from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, condecimal, constr
from typing import Optional, List

app = FastAPI()

class Item(BaseModel):
    name: constr(min_length=2, max_length=50)
    category: constr(min_length=3, max_length=20)
    description: Optional[constr(max_length=200)] = None
    price: condecimal(gt=0, max_digits=10, decimal_places=2)
    tax: Optional[condecimal(ge=0, max_digits=5, decimal_places=2)] = None

items_db = []
current_id = 0

@app.get("/")
def read_root():
    return {"message": "Welcome to TheDruidsHarvest API! <3"}

@app.get("/items/", response_model=List[Item])
def get_items():
    return items_db

@app.get("/items/{item_id}", response_model=dict)
def read_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items/", response_model=dict)
def create_item(item: Item):
    global current_id
    current_id += 1
    new_item = item.dict()
    new_item["id"] = current_id
    items_db.append(new_item)
    return new_item

@app.put("/items/{item_id}", response_model=dict)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items_db):
        if item["id"] == item_id:
            updated_item_data = updated_item.dict()
            updated_item_data["id"] = item_id
            items_db[index] = updated_item_data
            return updated_item_data
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(items_db):
        if item["id"] == item_id:
            del items_db[index]
            return {"message": f"Item {item_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")
