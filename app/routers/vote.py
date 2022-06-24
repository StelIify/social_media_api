from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db
from app.models import User
from app.oauth2 import get_current_user
from enum import Enum
from app import services
import asyncio
from time import perf_counter


class VoteDirection(Enum):
    ADD_VOTE = 1


router = APIRouter(tags=['Vote'])


@router.post('/vote', status_code=status.HTTP_201_CREATED)
async def vote(user_vote: schemas.Vote, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    post, post_to_vote = await asyncio.gather(services.get_post_by_id(user_vote.post_id, db), services.get_post_to_vote(user_vote, db, current_user))

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {user_vote.post_id} was not found")
    if user_vote.direction == VoteDirection.ADD_VOTE.value:
        if post_to_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} already voted on the post {user_vote.post_id}")
        return await services.register_new_vote(user_vote, db, current_user)
    else:
        if not post_to_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        return await services.delete_vote(db, post_to_vote)
