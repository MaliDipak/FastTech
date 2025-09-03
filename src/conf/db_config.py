import os

from sqlalchemy import create_engine

from constants import DATABASE_URL


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
