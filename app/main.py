from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routers.users import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
