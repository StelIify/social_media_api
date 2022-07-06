from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database import get_db
from sqlalchemy.orm import Session
from app.oauth2 import create_access_token
from app import services

router = APIRouter(tags=['Authentication'])


@router.post('/login')
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = await services.get_user_by_email(user_credentials, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    password_matched = user.check_password(user_credentials.password)

    if not password_matched:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = create_access_token(data={"user_id": user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}




