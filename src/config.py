from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta
import os

load_dotenv(Path(__file__).parent.parent / '.env')


class Config:
    SECRET_KEY: str                         = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI: str            = os.getenv('SQLALCHEMY_DATABASE_URI')
    ECHO: bool                              = bool(int(os.getenv('ECHO')))
    SQLALCHEMY_TRACK_MODIFICATIONS: bool    = bool(int(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')))
    SESSION_COOKIE_HTTPONLY: bool           = bool(int(os.getenv('SESSION_COOKIE_HTTPONLY')))
    SESSION_COOKIE_SAMESITE: str            = os.getenv('SESSION_COOKIE_SAMESITE')
    PERMANENT_SESSION_LIFETIME: timedelta   = timedelta(seconds=int(os.getenv('PERMANENT_SESSION_LIFETIME')))
