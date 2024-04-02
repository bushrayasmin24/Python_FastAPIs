from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime, time, timedelta
from uuid import UUID

app = FastAPI()


#lession-01 intro

# @app.get('/')
# async def root():
#     return {"message": "hello world"}

# @app.post('/')
# async def post():
#     return {"message": "hello from the post route"}

# @app.put('/')
# async def put():
#     return {"message": "hellow from the put route"}

# #lession-02 Path Parameters; Pydantic

# @app.get('/users')
# async def list_item():
#     return {"message": "list from route"}

# @app.get("/user/me")
# async def get_current_user():
#     return {"user_id": "This is the current user"}

# @app.get("/user/{user_id}")
# async def get_item(user_id: int):
#     return {"user_id": user_id}

# class FoodEnum(str, Enum):
#     fruits = "fruits"
#     vegetables = "vegetables"
#     dairy = "dairy"

# @app.get("/foods/{food_name}")
# async def get_food(food_name: FoodEnum):
#     if food_name == FoodEnum.vegetables:
#         return {"food_name": food_name, "message": "you are healthy"}

#     if food_name.value == "fruits":
#         return{
#             "food_name": food_name,
#             "message": "you are still healthy, but like sweet things."
#         }
    
# #lession-03 Query Parameters; Pydantic
    
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# @app.get("/items")
# async def list_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]

# @app.get("/items/{item_id}")
# async def get_item(item_id: str, q: Optional[str] = None, short: bool = False):      #3.10 -> q: str | None = None
#     item = {"item_id": item_id}
#     if q:
#         return {"item_id": item_id, "q": q}
    
#     if not short:
#         item.update(
#                 {  
#                      "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras vel."
#                 }
#             )
        
#     return {"item_id": item_id}

# @app.get("/users/{user_id}/items/{item_id}")
# async def get_user_item(sample_query_param: int, item_id: str, q: str | None = None, short: bool = False):
#     item = {"item_id": item_id, "sample_query_param": sample_query_param}
#     if q:
#         item.update({"q": q})
    
#     if not short:
#         item.update(
#                 {  
#                      "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras vel."
#                 }
#             )
        
#     return {"item_id": item_id}

# #lession-04 Request Body

# class Item(BaseModel):
#     name: str
#     description: Optional[str]= None
#     price: float
#     tax: float | None = None

# @app.post("/items")
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         prince_with_tax = item.price + item.tax
#         item_dict.update({"prince_with_tax": prince_with_tax})
#     return item_dict

# @app.put("/items/{item_id}")
# async def create_item_with_put(item_id: int, item: Item, q: str | None = None):
#     result = {"item_id": item_id, **item.dict()}
#     if q:
#         result.update({"q":q})
#     return result

# #lession-05 Query Parameters and String Validation

# @app.get("/items")
# async def read_items(q: str | None = Query("fixedquery", min_length=3, max_length=10, regex="^fixedquery$")):
#     result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Baz"}]}
#     if q:
#         result.update({"q":q})
#     return result

# @app.get("/items1")
# async def read_items1(q: str | None = Query(..., min_length=3, max_length=10, regex="^fixedquery$")):   #there have to be something ...
#     result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Baz"}]}
#     if q:
#         result.update({"q":q})
#     return result

# @app.get("/items2")
# async def read_items2(q: list[str] | None = Query(..., min_length=3, max_length=10, regex="^fixedquery$")):   #this will accept list
#     result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Baz"}]}
#     if q:
#         result.update({"q":q})
#     return result

# @app.get("/items3")
# async def read_items3(q: list[str] | None = Query(["foo", "bar"])):   #predefine value of q
#     result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Baz"}]}
#     if q:
#         result.update({"q":q})
#     return result

# @app.get("/items4")
# async def read_items4(
#     q: str 
#     | None = Query(
#         None, 
#         min_length=3, 
#         max_length=10, 
#         title="Sample query string", 
#         description="This is description.",
#         deprecated=True,
#         alias="item-query"
#         )
#     ): 
#     result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Baz"}]}
#     if q:
#         result.update({"q":q})
#     return result

# @app.get('/items_hidden')
# async def hidden_query_route(hidden_query: str | None = Query(None, include_in_schema=False)):
#     if hidden_query:
#         return {"hidden_query": hidden_query}
#     return {"hidden_query": "Not found"}

# #lession-05 Path Parameter and Numeric validation

# @app.get("/item_validation/{item_id}")
# async def read_items_validation(
#     item_id: int = Path(..., title="The ID of the item to get"), 
#     q: str | None = Query(None, alias='item-query')
#     ):
    
#     result = {"item_id": item_id}
#     if q:
#         result.update({"q":q})
#     return result

# @app.get("/item_validation1/{item_id}")
# async def read_items_validation1(
#     *,
#     item_id: int = Path(..., title="The ID of the item to get", ge=10, le=100), 
#     q: str = 'hello', 
#     size: float = Query(..., gt=0, lt=7.75)
#     ):
    
#     result = {"item_id": item_id}
#     if q:
#         result.update({"q":q})
#     return result

#lession-07 Body Multiple Parameter

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     prince: float
#     tax: float | None = None

# class User(BaseModel):
#         user_name: str
#         full_name: str | None = None

# class Importance:                 #in this place uuse Body
#      importance: int

# @app.put("/items/{item_id}")
# async def update_item(
#         *,
#         item_id: int = Path(..., title="The ID of the item to get", ge=0, le=150),
#         q: str | None = None,
#         item: Item | None = None,
#         user: User,
#         importance: int = Body(..., embed=True)
# ):
#     results = {"item_id": item_id}
#     if q: 
#         results.update({"q": q})

#     if item:
#         results.update({"item": item})
    
#     if user:
#          results.update({"user": user})

#     if importance:
#         results.update({"importance": importance})

#     return results

#lession-08 Body Fields

# class Item(BaseModel):
#     name: str
#     descroption: str | None = Field(
#         None, title="the description of the item", max_length =300
#     )
#     price: float = Field(..., gt=0, description="The price must be greater than zero.")
#     tax: float | None = None

# @app.put("/items/{item_id}")
# async def update_item(
#         item_id: int,
#         item: Item = Body(...)
# ):
#     results = {"item_id": item_id, "item": item}    
#     return results

#lession-09 Nesting Models in request body

# class Image(BaseModel):
#     url: HttpUrl
#     name: str

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#     tags: set[str] = []
#     image: list[Image] | None = None

# class Offer(BaseModel):
#     name: str
#     description:str | None = None
#     price: float
#     items: list[Item]

# @app.put("/items/{item_id}")
# async def update_item(
#         item_id: int,
#         item: Item
# ):
#     results = {"item_id": item_id, "item": item}    
#     return results

# @app.post("/offers")
# async def create_offer(offer: Offer = Body(..., ambed=True)):
#     return offer

# @app.post("/images/multiple")
# async def create_multiple_images(images: list[Image] = Body(..., ambed=True)):
#     return images

# @app.post("/blah")
# async def create_blah(blahs: dict[int, float]):
#     return blahs

#lession-10 Declare request example data

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

# class Config:
#     schema_extra = {
#         "example": {
#             "name": "Foo",
#             "description": "A very nice Item",
#             "price": 16.25,
#             "tax": 1.167
#         }
#     }

# @app.put("/items/{item_id}")
# async def update_item(
#         item_id: int,
#         item: Item
# ):
#     results = {"item_id": item_id, "item": item}    
#     return results

# @app.put("/items/{item_id}")
# async def update_item01(
#         item_id: int,
#         item: Item = Body(
#             ...,
#          examples={
#             "normal": {
#                 "summary": "A normal example",
#                 "description": "A __normal__ item works _correctly_",
#                 "value": {
#                     "name": "Foo",
#                     "description": "A very nice Item",
#                     "price": 16.25,
#                     "tax": 1.67,
#                 },
#             },
#             "converted": {
#                 "summary": "An example with converted data",
#                 "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
#                 "value": {"name": "Bar", "price": "16.25"},
#             },
#             "invalid": {
#                 "summary": "Invalid data is rejected with an error",
#                 "description": "Hello youtubers",
#                 "value": {"name": "Baz", "price": "sixteen point two five"},
#             },
#         },
#     ),
# ):
#     results = {"item_id": item_id, "item": item}    
#     return results

#lession-10 Extra data types

# @app.put("/items/{item_id}")
# async def update_item(
#         item_id: UUID,
#         start_date: datetime | None = Body(None),
#         end_date: time | None = Body(None),
#         repeat_at: time | None = Body(None),
#         process_after: timedelta | None = Body(None),
# ):
#     start_process = start_date - process_after
#     duration = end_date - start_process

#     results = {"item_id": item_id, 
#                "start_date": start_date,
#                "end_date": end_date,
#                "repeat_at": repeat_at,
#                "start_process": start_process,
#                "duration": duration}    
#     return results

#lession-11 Extra data types

@app.get("/items")
async def read_items(
    cookie_id: str | None = Cookie(None),
    accept_encoding: str | None = Header(None, convert_underscores=False),
    sec_ch_ua: str | None = Header(None),
    user_agent: str | None = Header(None),
    x_token: list[str] | None = Header(None)
):
    return {
        "cookie_id": cookie_id,
        "accept_encoding": accept_encoding,
        "sec-ch-ue": sec_ch_ua,
        "user_agent": user_agent,
        "x_token": x_token
        }

#lession-11 Response Model

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: Literal["foo", "bar", "baz"]):
    return items[item_id]

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user

@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: Literal["foo", "bar", "baz"]):
    return items[item_id]

@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_items_public_data(item_id: Literal["foo", "bar", "baz"]):
    return items[item_id]