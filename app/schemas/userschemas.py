from pydantic import BaseModel, Field
from typing import Optional, List

# Pydantic Schemas
class UserCreate(BaseModel):
    name: str
    email: str
    contact: str
    password: str

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    contact: str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    contact: str | None = None
    password: str | None = None
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
