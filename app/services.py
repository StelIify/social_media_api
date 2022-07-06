from sqlalchemy.orm import Session
from .schemas import UserCreate, Vote
from app import models

# User Services


async def register_new_user(user_request: UserCreate, db: Session):
    new_user = models.User(**user_request.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


async def get_user_by_id(id, db: Session):
    return db.query(models.User).filter(models.User.id == id).first()


async def get_user_by_email(user_credentials, db: Session):
    return db.query(models.User).filter(models.User.email == user_credentials.username).first()


# Post Services


async def get_post_by_id(post_id: int, db: Session):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


# Vote Services


async def get_post_to_vote(user_vote: Vote, db: Session, current_user: models.User):
    return db.query(models.Vote).filter(models.Vote.post_id == user_vote.post_id, models.Vote.user_id == current_user.id).first()


async def register_new_vote(user_vote: Vote, db: Session, current_user: models.User) -> dict:
    new_vote = models.Vote(user_id=current_user.id, post_id=user_vote.post_id)
    db.add(new_vote)
    db.commit()

    return {"message": "successfully added vote"}


async def delete_vote(db: Session, post):
    db.delete(post)
    db.commit()
    return {"message": "successfully deleted vote"}