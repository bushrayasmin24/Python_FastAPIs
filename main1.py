from fastapi import (
    FastAPI, 
    Query, 
    Path, 
    Body, 
    Cookie, 
    Header,
    status, 
    Form,
    File,
    UploadFile,
    HTTPException,
    Request,
)
from enum import Enum
from typing import Optional, Literal, Union
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from datetime import datetime, time, timedelta
from uuid import UUID
from starlette.response import HTMLResponse

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

# Part 14 - Extra Models
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str

def fake_password_hasher(raw_password: str):
    return f"supersecret{raw_password}"

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User 'saved'.")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type = "car"

class PlaneItem(BaseItem):
    type = "plane"
    size: int

items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: Literal["item1", "item2"]):
    return items[item_id]

class ListItem(BaseModel):
    name: str
    description: str

list_items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

@app.get("/list_items/", response_model=list[ListItem])
async def read_items():
    return items

@app.get("/arbitrary", response_model=dict[str, float])
async def get_arbitrary():
    return {"foo": 1, "bar": "2"}

## Part 15 - Response Status Codes
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}


@app.delete("/items/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(pk: str):
    print("pk", pk)
    return pk


@app.get("/items/", status_code=status.HTTP_302_FOUND)
async def read_items_redirect():
    return {"hello": "world"}

# Part 16 - Form Fields
@app.post("/login/")
async def login(username: str = Form(...), password: str = Body(...)):
    print("password", password)
    return {"username": username}


@app.post("/login-json/")
async def login_json(username: str = Body(...), password: str = Body(...)):
    print("password", password)
    return {"username": username}

# Part 17 - Request Files

@app.post("/files/")
async def create_file(
    files: list[bytes] = File(..., description="A file read as bytes")
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfile/")
async def create_upload_file(
    files: list[UploadFile] = File(..., description="A file read as UploadFile")
):
    return {"filename": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

# Part 18 - Request Forms and Files
@app.post("/files/")
async def create_file(
    file: bytes = File(...),
    fileb: UploadFile = File(...),
    token: str = Form(...),
    hello: str = Body(...),
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
        "hello": hello,
    }

# Part 19 - Handling Errors
items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorns(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return PlainTextResponse(str(exc), status_code=400)
#
#
# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
#
#
# @app.get("/validation_items/{item_id}")
# async def read_validation_items(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
#     return {"item_id": item_id}


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors(), "blahblah": exc.body}),
#     )
#
#
# class Item(BaseModel):
#     title: str
#     size: int
#
#
# @app.post("/items/")
# async def create_item(item: Item):
#     return item


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/blah_items/{item_id}")
async def read_items(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}

# Part 20 - Path Operation Configuration
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


class Tags(Enum):
    items = "items"
    users = "users"


@app.post(
    "/items/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.items],
    summary="Create an Item-type item",
    # description="Create an item with all the information: "
    # "name; description; price; tax; and a set of "
    # "unique tags",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


@app.get("/items/", tags=[Tags.items])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=[Tags.users])
async def read_users():
    return [{"username": "PhoebeBuffay"}]


@app.get("/elements/", tags=[Tags.items], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]