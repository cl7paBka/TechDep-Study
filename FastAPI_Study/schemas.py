from pydantic import BaseModel


class TrainSchema(BaseModel):
    first_row: str
    second_row: str


class UserInfo(BaseModel):
    name: str
    first_name: str
    age: int