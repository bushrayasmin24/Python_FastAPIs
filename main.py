from fastapi import FastAPI, Query, Path
from enum import Enum
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


#lession-01 intro

@app.get('/')
async def root():
    return {"message": "hello world"}

@app.post('/')
async def post():
    return {"message": "hello from the post route"}

@app.put('/')
async def put():
    return {"message": "hellow from the put route"}

#lession-02 Path Parameters; Pydantic

@app.get('/users')
async def list_item():
    return {"message": "list from route"}

@app.get("/user/me")
async def get_current_user():
    return {"user_id": "This is the current user"}

@app.get("/user/{user_id}")
async def get_item(user_id: int):
    return {"user_id": user_id}

class FoodEnum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"

@app.get("/foods/{food_name}")
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {"food_name": food_name, "message": "you are healthy"}

    if food_name.value == "fruits":
        return{
            "food_name": food_name,
            "message": "you are still healthy, but like sweet things."
        }
    
#lession-03 Query Parameters; Pydantic
    
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items")
async def list_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]

@app.get("/items/{item_id}")
async def get_item(item_id: str, q: Optional[str] = None, short: bool = False):      #3.10 -> q: str | None = None
    item = {"item_id": item_id}
    if q:
        return {"item_id": item_id, "q": q}
    
    if not short:
        item.update(
                {  
                     "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras vel."
                }
            )
        
    return {"item_id": item_id}

@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(sample_query_param: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "sample_query_param": sample_query_param}
    if q:
        item.update({"q": q})
    
    if not short:
        item.update(
                {  
                     "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras vel."
                }
            )
        
    return {"item_id": item_id}

#lession-04 Request Body

class Item(BaseModel):
    name: str
    description: Optional[str]= None
    price: float
    tax: float | None = None

@app.post("/items")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        prince_with_tax = item.price + item.tax
        item_dict.update({"prince_with_tax": prince_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def create_item_with_put(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q":q})
    return result

#lession-05 Query Parameters and String Validation

@app.get("/items")
async def read_items(q: str | None = Query("fixedquery", min_length=3, max_length=10, regex="^fixedquery$")):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Baz"}]}
    if q:
        result.update({"q":q})
    return result

@app.get("/items1")
async def read_items1(q: str | None = Query(..., min_length=3, max_length=10, regex="^fixedquery$")):   #there have to be something ...
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Baz"}]}
    if q:
        result.update({"q":q})
    return result

@app.get("/items2")
async def read_items2(q: list[str] | None = Query(..., min_length=3, max_length=10, regex="^fixedquery$")):   #this will accept list
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Baz"}]}
    if q:
        result.update({"q":q})
    return result

@app.get("/items3")
async def read_items3(q: list[str] | None = Query(["foo", "bar"])):   #predefine value of q
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Baz"}]}
    if q:
        result.update({"q":q})
    return result

@app.get("/items4")
async def read_items4(
    q: str 
    | None = Query(
        None, 
        min_length=3, 
        max_length=10, 
        title="Sample query string", 
        description="This is description.",
        deprecated=True,
        alias="item-query"
        )
    ): 
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Baz"}]}
    if q:
        result.update({"q":q})
    return result

@app.get('/items_hidden')
async def hidden_query_route(hidden_query: str | None = Query(None, include_in_schema=False)):
    if hidden_query:
        return {"hidden_query": hidden_query}
    return {"hidden_query": "Not found"}

#lession-05 Path Parameter and Numeric validation

@app.get("/item_validation/{item_id}")
async def read_items_validation(
    item_id: int = Path(..., title="The ID of the item to get"), 
    q: str | None = Query(None, alias='item-query')
    ):
    
    result = {"item_id": item_id}
    if q:
        result.update({"q":q})
    return result

@app.get("/item_validation1/{item_id}")
async def read_items_validation1(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=10, le=100), 
    q: str = 'hello', 
    size: float = Query(..., gt=0, lt=7.75)
    ):
    
    result = {"item_id": item_id}
    if q:
        result.update({"q":q})
    return result