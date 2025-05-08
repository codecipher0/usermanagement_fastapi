from sqlalchemy.orm import Session
from typing import Type, TypeVar, List, Optional

T = TypeVar('T')

class BaseController:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, model: Type[T], skip: int = 0, limit: int = 10) -> List[T]:
        return self.db.query(model).filter(getattr(model, "is_deleted", False) == False).offset(skip).limit(limit).all()

    def get_by_id(self, model: Type[T], id: int) -> Optional[T]:
        return self.db.query(model).filter(model.id == id, getattr(model, "is_deleted", False) == False).first()

    def create(self, instance: T) -> T:
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, instance: T) -> None:
        if hasattr(instance, "is_deleted"):
            instance.is_deleted = True
        else:
            self.db.delete(instance)
        self.db.commit()