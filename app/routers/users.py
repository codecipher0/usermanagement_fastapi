from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..models import models
from ..core import auth
from ..schemas import userschemas
from ..core.database import get_db

router = APIRouter()

@router.post("/token", response_model=userschemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username, models.User.is_deleted == False).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=userschemas.UserRead)
def create_user(user: userschemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(name=user.name, email=user.email, contact=user.contact, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=list[userschemas.UserRead])
def read_users(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    users = db.query(models.User).filter(models.User.is_deleted == False).all()
    return users

@router.get("/users/{user_id}", response_model=userschemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id, models.User.is_deleted == False).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=userschemas.UserRead)
def update_user(user_id: int, user_update: userschemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
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