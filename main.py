from typing import Optional

from fastapi import FastAPI, status
from datetime import date
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    path = request.url.path
    if path == '/items' and request.method == 'GET':
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": "Well you thought it was over"}),
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items")
def read_items(q: Optional[int] = None):
    return {"message": "So you want to read everything haha"}


@app.post("/items")
def post_items(q: Optional[int] = None):
    return {"message": "So you want to read everything haha"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/date/{date_str}")
def read_date(date_str: date):
    return {
        "year": date_str.year,
        "month": date_str.month
    }


@app.post("/item/")
def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    return item_dict
