from fastapi import Response, status, HTTPException, Depends, FastAPI, APIRouter
from app import models, schemas
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import User
from typing import List, Optional
from app.oauth2 import get_current_user

router = APIRouter(tags=['Posts'])


@router.get('/posts', response_model=List[schemas.PostResponseWithVotes])
async def get_posts(db: Session = Depends(get_db), limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get('/posts/{id}', response_model=schemas.PostResponseWithVotes)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(
        models.Post.id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post


@router.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_post = models.Post(author_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if post.author != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform requested action")

    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/posts/{id}')
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()

    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if post_to_update.author != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform requested action")

    post_query.update(post.dict())  # update with data from the user

    db.commit()
    db.refresh(post_to_update)

    return post_to_update


@router.post('/posts/{id}/comments', response_model=schemas.CommentResponse)
def create_comment(id: int, comment: schemas.CommentBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    new_comment = models.Comment(author_id=current_user.id, post_id=post.id, **comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

