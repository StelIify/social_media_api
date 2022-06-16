from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserCommentInfo(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(UserBase):
    pass
