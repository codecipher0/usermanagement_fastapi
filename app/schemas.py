from pydantic import BaseModel, Field
from typing import Optional, List, ForwardRef

CommentReadRef = ForwardRef("CommentRead")

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
    
class CommentCreate(BaseModel):
    comment: str
    parent_id: Optional[int] = None
    
class CommentRead(BaseModel):
    id: int
    user_id: int
    parent_id: Optional[int] = None
    comment: str
    replies: List[CommentReadRef] = Field(default_factory=list)
    
    class Config:
        orm_mode = True

CommentRead.update_forward_refs()
    
