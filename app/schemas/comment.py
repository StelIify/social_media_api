from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from .user import UserCommentInfo


class CommentBase(BaseModel):
    message: str


class CommentResponse(BaseModel):
    id: int
    author: UserCommentInfo
    message: str
    created_at: datetime

    class Config:
        orm_mode = True
