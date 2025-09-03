from fastapi import FastAPI

from src.conf.db_config import engine
from src.router import user_router
from src.model.declarative_base import Base


# create db
Base.metadata.create_all(engine)


# create app
app = FastAPI()


# configure routes 
app.include_router(user_router.router)

