from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: EmailStr


class UserInfo(BaseModel):  # Эта схема нужна для динамического изменения SQL запроса
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None


class UserInDB(UserInfo):
    user_id: int
