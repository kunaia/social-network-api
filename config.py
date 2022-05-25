import os
import datetime

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.environ.get("DEBUG", "False") == "True"
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{os.environ.get("DATABASE_USER")}:' \
                              f'{os.environ.get("DATABASE_USER_PASSWORD")}@{os.environ.get("DATABASE_HOST")}' \
                              f'/{os.environ.get("DATABASE_NAME")}'
