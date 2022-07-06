from fastapi import status, HTTPException, Depends, APIRouter
from app import utils, schemas
from app.database import get_db
from sqlalchemy.orm import Session
from app import services

router = APIRouter(tags=['Users'])


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user_request: schemas.UserCreate, db: Session = Depends(get_db)):
    user = await utils.verify_email_exist(user_request.email, db)

    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The user with this id already exists in the system")

    new_user = await services.register_new_user(user_request, db)

    return new_user


@router.get('/users/{id}', response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = await services.get_user_by_id(id, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    return user
