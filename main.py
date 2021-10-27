from typing import Optional

from fastapi import FastAPI
from datetime import date

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/date/{date_str}")
def read_date(date_str: date):
    return {
        "year": date_str.year,
        "month": date_str.month
    }
