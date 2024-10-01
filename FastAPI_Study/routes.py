from fastapi import APIRouter
from schemas import TrainSchema, UserInfo
from random import randint

api_router = APIRouter()


@api_router.get('/hello')
def hello():
    return {'name': 'Макс'}


@api_router.get('/random-int')
def random_int():
    return {"integer": randint(0, 101)}


@api_router.post("/skley")
def skley(
        input_data: TrainSchema  # Схема ввода данных. Нам приходит 2 строки
):
    first_row = input_data.first_row  # Инициализируем 1 строку
    second_row = input_data.second_row  # Инициализируем 2 строку
    return {"new_row": first_row + second_row}


@api_router.post("/user-info")
def user_info(input_data: UserInfo):
    name = input_data.name
    first_name = input_data.first_name
    age = input_data.age
    return {
        "name": name,
        "first_name": first_name,
        "age": age
    }
