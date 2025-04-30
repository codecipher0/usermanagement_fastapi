from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://jay:pass1234@localhost:3306/bluecube_users"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()