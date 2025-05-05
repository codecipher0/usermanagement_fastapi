from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, auth
from ..schemas import commentschemas
from ..database import get_db

comment_router = APIRouter()
    
@comment_router.post("/comments/", response_model=commentschemas.CommentRead)
def add_comment(comment: commentschemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_comment = models.Comment(user_id=current_user.id, comment=comment.comment, parent_id=comment.parent_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def build_comment_tree(comment, db):
    replies = db.query(models.Comment).filter(models.Comment.parent_id == comment.id, models.Comment.is_deleted == False).all()
    return commentschemas.CommentRead(
        id=comment.id,
        user_id=comment.user_id,
        comment="[deleted]" if comment.is_deleted else comment.comment,
        parent_id=comment.parent_id,
        replies=[build_comment_tree(reply, db) for reply in replies]
    )
    
@comment_router.get("/comments/", response_model=list[commentschemas.CommentRead])
def read_comments(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0), db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(models.Comment.parent_id == None, models.Comment.is_deleted == False).offset(skip).limit(limit).all()
    #return comments
    return [build_comment_tree(comment, db) for comment in comments]
    
@comment_router.get("/comments/{comment_id}", response_model=commentschemas.CommentRead)
def read_comment(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    #comments = db.query(models.Comment).filter((models.Comment.id == comment_id) | (models.Comment.parent_id == comment_id)).offset(skip).limit(limit).all()
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id, models.Comment.is_deleted == False).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    #return comments
    return build_comment_tree(comment, db)
    #return [build_comment_tree(comments, db) for comment in comments]

@comment_router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id, models.Comment.user_id == current_user.id, models.Comment.is_deleted == False).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or not yours")
    comment.is_deleted = True
    db.commit()
    return {"detail": "Comment deleted"}
