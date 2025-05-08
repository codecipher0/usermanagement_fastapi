from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..models import models
from ..core import auth
from ..schemas import commentschemas
from ..core.database import get_db
from ..controllers.commentcontroller import CommentController

router = APIRouter()
    
@router.post("/", response_model=commentschemas.CommentRead)
def add_comment(comment: commentschemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    comment_ctrl = CommentController(db)
    return comment_ctrl.create_comment(current_user.id, comment)
    
@router.get("/", response_model=list[commentschemas.CommentRead])
def read_comments(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0), db: Session = Depends(get_db)):
    comment_ctrl = CommentController(db)
    comments = comment_ctrl.get_comments(skip,limit)
    return [comment_ctrl.build_comment_tree(comment) for comment in comments]
    
@router.get("/{comment_id}", response_model=commentschemas.CommentRead)
def read_comment(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    comment_ctrl = CommentController(db)
    comment = comment_ctrl.get_comment_by_id(comment_id)
    return comment_ctrl.build_comment_tree(comment)

@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    comment_ctrl = CommentController(db)
    comment_ctrl.delete_comment(comment_id)
    return {"detail": "Comment deleted"}
