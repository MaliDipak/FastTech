from sqlalchemy.orm import sessionmaker

from src.conf.db_config import engine


Session = sessionmaker(bind=engine)
session = Session()