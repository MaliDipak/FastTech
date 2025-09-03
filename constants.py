import os

from dotenv import load_dotenv


# Load .env file
load_dotenv()


BASE_DIR = os.path.dirname(__file__)
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'db', os.getenv('DEV_DATABASE_URL'))}"
LOG_FILE_PATH = os.path.join(BASE_DIR, "log", "app.log")
SECRET_KEY = os.getenv("SECRET_KEY")

