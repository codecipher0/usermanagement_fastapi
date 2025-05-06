from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from ..core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    contact = Column(String(50), nullable=True)
    hashed_password = Column(String(100), nullable=False)
    is_deleted = Column(Boolean, default=False)
    
class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    comment = Column(Text, nullable=False)
    is_deleted = Column(Boolean, default=False)
    
    #user = relationship("User", back_populates="comments")
    #replies = relationship("Comment", back_populates="children")
    #children = relationship("Comment", back_populates="replies", remote_side=[id])    