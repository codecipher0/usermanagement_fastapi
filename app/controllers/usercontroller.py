from fastapi import HTTPException, status
from ..models import models
from ..core import auth
from ..schemas import userschemas
from .basecontroller import BaseController
from typing import List

class UserController(BaseController):
    def get_user_by_email(self, email: str):
        return self.db.query(models.User).filter(models.User.email == email, models.User.is_deleted == False).first()
    
    def get_user_by_id(self, user_id: int):
        user = self.db.query(models.User).filter(models.User.id == user_id, models.User.is_deleted == False).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    def create_user(self, user: userschemas.UserCreate):
        hashed_password = auth.get_password_hash(user.password)
        db_user = models.User(name=user.name, email=user.email, contact=user.contact, hashed_password=hashed_password)
        return self.create(db_user)
    
    def update_user(self, user_id: int, user_update: userschemas.UserUpdate):
        user = self.get_user_by_id(user_id)
        update_data = user_update.dict(exclude_unset=True)
        return self.update(user, update_data)
        
    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        self.delete(user)
        return user
        
    def get_users(self, skip: int = 0, limit: int = 10) -> List[models.User]:
        return self.get_all(models.User, skip, limit)