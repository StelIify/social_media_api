from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate, Vote
from app import models
from fastapi import Response, status


async def register_new_user(user_request: UserCreate, db: Session):
    new_user = User(**user_request.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


async def get_user_by_id(id, db: Session):
    return db.query(User).filter(User.id == id).first()


async def get_post_by_id(user_vote: Vote, db: Session):
    return db.query(models.Post).filter(models.Post.id == user_vote.post_id).first()


async def get_post_to_vote(user_vote: Vote, db: Session, current_user: User):
    return db.query(models.Vote).filter(models.Vote.post_id == user_vote.post_id, models.Vote.user_id == current_user.id).first()


async def register_new_vote(user_vote: Vote, db: Session, current_user: User) -> dict:
    new_vote = models.Vote(user_id=current_user.id, post_id=user_vote.post_id)
    db.add(new_vote)
    db.commit()

    return {"message": "successfully added vote"}


async def delete_vote(db: Session, post):
    db.delete(post)
    db.commit()
    return {"message": "successfully deleted vote"}