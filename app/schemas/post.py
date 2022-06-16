from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserResponse
from app.schemas.comment import CommentResponse


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    published: bool


class PostResponse(PostBase):
    id: int
    created_at: datetime
    author: UserResponse
    comments: List[CommentResponse] = []

    class Config:
        orm_mode = True


class PostResponseWithVotes(BaseModel):
    Post: PostResponse
    votes: int
