# Install needed packages first:
# pip install fastapi uvicorn sqlalchemy pymysql

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel

# Database config
DATABASE_URL = "mysql+pymysql://jay:pass1234@localhost:3306/bluecube_users"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    contact = Column(String(50), nullable=True)

# Pydantic Schemas
class UserCreate(BaseModel):
    name: str
    email: str
    contact: str

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

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email, contact=user.contact)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[UserRead])
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.name is not None:
        user.name = user_update.name
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.contact is not None:
        user.contact = user_update.contact

    db.commit()
    db.refresh(user)
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}
