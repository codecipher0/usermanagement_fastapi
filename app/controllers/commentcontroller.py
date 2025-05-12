from fastapi import HTTPException
from ..models import models
from ..schemas import commentschemas
from .basecontroller import BaseController
from typing import List

class CommentController(BaseController):
    def get_comment_by_id(self, comment_id: int):
        comment = self.db.query(models.Comment).filter(models.Comment.id == comment_id, models.Comment.is_deleted == False).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment

    def create_comment(self, user_id: int, comment: commentschemas.CommentCreate):
        if comment.parent_id:
            parent = self.db.query(models.Comment).filter(models.Comment.id == comment.parent_id, models.Comment.is_deleted == False).first()
            if not parent:
                raise HTTPException(status_code=400, detail="Parent comment not found")
        db_comment = models.Comment(user_id=user_id, comment=comment.comment, parent_id=comment.parent_id)
        return self.create(db_comment)

    def build_comment_tree(self, comment):
        replies = self.db.query(models.Comment).filter(models.Comment.parent_id == comment.id, models.Comment.is_deleted == False).all()
        return commentschemas.CommentRead(
            id=comment.id,
            user_id=comment.user_id,
            comment="[deleted]" if comment.is_deleted else comment.comment,
            parent_id=comment.parent_id,
            replies=[self.build_comment_tree(reply) for reply in replies]
        )

    def get_comments(self, skip: int = 0, limit: int = 10) -> List[models.Comment]:
        return self.db.query(models.Comment).filter(models.Comment.is_deleted == False, models.Comment.parent_id == None).offset(skip).limit(limit).all()

    def delete_comment(self, comment_id: int):
        comment = self.get_comment_by_id(comment_id)
        self.delete(comment)
        return comment
        
    def get_comments_by_user_id(self, user_id: int, skip: int = 0, limit: int = 10) -> List[models.Comment]:
        return self.db.query(models.Comment).filter(models.Comment.user_id == user_id, models.Comment.is_deleted == False).offset(skip).limit(limit).all()