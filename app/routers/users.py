from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..models import models
from ..core import auth
from ..schemas import userschemas
from ..core.database import get_db
from ..controllers.usercontroller import UserController

router = APIRouter()

@router.post("/token", response_model=userschemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #user = db.query(models.User).filter(models.User.email == form_data.username, models.User.is_deleted == False).first()
    user_ctrl = UserController(db)
    user = user_ctrl.get_user_by_email(email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", response_model=userschemas.UserRead)
def create_user(user: userschemas.UserCreate, db: Session = Depends(get_db)):
    user_ctrl = UserController(db)
    db_user = user_ctrl.create_user(user)
    return db_user

@router.get("/", response_model=list[userschemas.UserRead])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    user_ctrl = UserController(db)
    return user_ctrl.get_users(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=userschemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    user_ctrl = UserController(db)
    user = user_ctrl.get_user_by_id(user_id)
    return user

@router.put("/{user_id}", response_model=userschemas.UserRead)
def update_user(user_id: int, user_update: userschemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    user_ctrl = UserController(db)
    user = user_ctrl.update_user(user_id, user_update)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_ctrl = UserController(db)
    return {"detail": "User deleted"}