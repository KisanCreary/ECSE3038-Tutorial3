from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

app = FastAPI()

# In-memory storage for fruits
fruits_db = []
current_id = 1  # To generate unique IDs for fruits

# Pydantic model for Fruit 
class Fruit(BaseModel):
    id: Optional[int] = None
    name: str
    variety: str
    quantity: int
    supplier: str
    harvest_date: datetime
    creation_date: Optional[datetime] = None
    available: bool = True
    price: float

# Helper function to find a fruit by ID
def find_fruit_by_id(fruit_id: int):
    for fruit in fruits_db:
        if fruit["id"] == fruit_id:
            return fruit
    return None

# GET all available fruits
@app.get("/api/fruits", response_model=List[Fruit])
async def get_all_fruits():
    available_fruits = [fruit for fruit in fruits_db if fruit["available"]]
    return available_fruits

# GET a single fruit by ID
@app.get("/api/fruits/{fruit_id}", response_model=Fruit)
async def get_fruit(fruit_id: int):
    fruit = find_fruit_by_id(fruit_id)
    if not fruit or not fruit["available"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fruit not found"
        )
    return fruit

# POST a new fruit
@app.post("/api/fruits", status_code=status.HTTP_201_CREATED, response_model=Fruit)
async def add_fruit(fruit: Fruit):
    global current_id
    fruit_dict = fruit.dict()
    fruit_dict["id"] = current_id
    fruit_dict["creation_date"] = datetime.now()  # Set creation date on the server side
    fruits_db.append(fruit_dict)
    current_id += 1
    return fruit_dict

# PATCH a fruit to update availability, price, or quantity
@app.patch("/api/fruits/{fruit_id}")
async def update_fruit(
    fruit_id: int,
    available: Optional[bool] = None,
    price: Optional[float] = None,
    quantity: Optional[int] = None
):
    fruit = find_fruit_by_id(fruit_id)
    if not fruit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fruit not found"
        )

    # Update availability if provided
    if available is not None:
        fruit["available"] = available

    # Update price and quantity only if the fruit is available
    if fruit["available"]:
        if price is not None:
            fruit["price"] = price
        if quantity is not None:
            fruit["quantity"] = quantity

    # Always return available along with price and quantity if available is true
    response = {"available": fruit["available"]}

    # If the fruit is available, always return price and quantity
    if fruit["available"]:
        response["price"] = fruit["price"]
        response["quantity"] = fruit["quantity"]

    # If fruit is unavailable, return only available
    if not fruit["available"]:
        response = {"available": fruit["available"]}

    return response


# DELETE a fruit (set availability to false)
@app.delete("/api/fruits/{fruit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fruit(fruit_id: int):
    fruit = find_fruit_by_id(fruit_id)
    if not fruit or not fruit["available"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fruit not found"
        )
    fruit["available"] = False