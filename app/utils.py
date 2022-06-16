from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def verify_email_exist(user_email: str, db: Session):
    return db.query(models.User).filter(models.User.email == user_email).first()

