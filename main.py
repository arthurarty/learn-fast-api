from typing import Optional

from fastapi import FastAPI, status, UploadFile, File, Depends
from datetime import date
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.requests import Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Callable, List
from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile
from pydantic import BaseModel
from datetime import datetime


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
    current_date = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
    return {"detail": f"Hello World: {current_date}"}


@app.get("/items")
def read_items(q: Optional[int] = None):
    return {"detail": "So you want to read everything haha"}


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


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(None)):
    tmp_path = save_upload_file_tmp(file)
    return {"filename": file.filename, "tmp_path": tmp_path}


def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


def do_sum(x: Optional[str] = 'that thing'):
    print('Value of x is')
    return f'That value was {x}'


@app.get('/test_depends/{input_str}', )
def use_depends(input_str, user_name: str = Depends(do_sum)):
    return {
        'input_str': input_str,
        'user_name': user_name
    }


class UserInput(BaseModel):
    ids: List[int]
    name: str
    age: int


@app.post('/inputData')
def submit_user_data(user_input: UserInput):
    return user_input


@app.post('/display_data')
async def display_data(data: dict):
    return data
