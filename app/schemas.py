from pydantic import BaseModel

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
    
class CommentRead(BaseModel):
    id: int
    user_id: int
    original_comment_id: int
    comment: str
    
    class Config:
        orm_mode = True
        
class ReplyCreate(BaseModel):
    original_comment_id: int
    reply: str