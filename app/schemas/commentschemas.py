from pydantic import BaseModel, Field
from typing import Optional, List

# Pydantic Schemas
    
class CommentCreate(BaseModel):
    comment: str
    parent_id: Optional[int] = None
    
class CommentRead(BaseModel):
    id: int
    user_id: int
    comment: str
    parent_id: Optional[int] = None
    replies: List['CommentRead'] = []
    
    class Config:
        orm_mode = True

CommentRead.update_forward_refs()
    
