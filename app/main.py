from fastapi import FastAPI
from .core.database import Base, engine
from .models import models
from .routers.routers import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router, prefix="/api")
