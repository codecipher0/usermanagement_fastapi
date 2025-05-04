from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter()

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username, models.User.is_deleted == False).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(name=user.name, email=user.email, contact=user.contact, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=list[schemas.UserRead])
def read_users(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    users = db.query(models.User).filter(models.User.is_deleted == False).all()
    return users

@router.get("/users/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id, models.User.is_deleted == False).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id, models.User.is_deleted == False).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.name is not None:
        user.name = user_update.name
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.contact is not None:
        user.contact = user_update.contact
    if user_update.password is not None:
        user.hashed_password = auth.get_password_hash(user_update.password)


    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id, models.User.is_deleted == False).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    #db.delete(user)
    user.is_deleted = True
    db.commit()
    return {"detail": "User deleted"}
    
@router.post("/comments/", response_model=schemas.CommentRead)
def add_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_comment = models.Comment(user_id=current_user.id, comment=comment.comment, parent_id=comment.parent_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def build_comment_tree(comment, db):
    replies = db.query(models.Comment).filter(models.Comment.parent_id == comment.id, models.Comment.is_deleted == False).all()
    return schemas.CommentRead(
        id=comment.id,
        user_id=comment.user_id,
        comment="[deleted]" if comment.is_deleted else comment.comment,
        parent_id=comment.parent_id,
        replies=[build_comment_tree(reply, db) for reply in replies]
    )
    
@router.get("/comments/", response_model=list[schemas.CommentRead])
def read_comments(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0), db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(models.Comment.parent_id == None, models.Comment.is_deleted == False).offset(skip).limit(limit).all()
    #return comments
    return [build_comment_tree(comment, db) for comment in comments]
    
@router.get("/comments/{comment_id}", response_model=schemas.CommentRead)
def read_comment(comment_id: int, skip: int = Query(0, ge=0), limit: int = Query(10, gt=0), db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    #comments = db.query(models.Comment).filter((models.Comment.id == comment_id) | (models.Comment.parent_id == comment_id)).offset(skip).limit(limit).all()
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id, models.Comment.is_deleted == False).offset(skip).limit(limit).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    #return comments
    return build_comment_tree(comment, db)
    #return [build_comment_tree(comments, db) for comment in comments]
    
#@router.post("/reply/", response_model=schemas.CommentRead)
#def add_reply(reply: schemas.ReplyCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
#    db_reply = models.Comment(user_id=current_user.id, parent_id=reply.parent_id, comment=reply.reply)
#    db.add(db_reply)
#    db.commit()
#    db.refresh(db_reply)
#    return db_reply

@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id, models.Comment.user_id == current_user.id, models.Comment.is_deleted == False).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or not yours")
    comment.is_deleted = True
    db.commit()
    return {"detail": "Comment deleted"}
