from __future__ import annotations

from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta
from dataclasses import dataclass
from tomllib import load
import os

load_dotenv(Path(__file__).parent.parent / '.env')


class Config:
    SECRET_KEY: str                         = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI: str            = os.getenv('SQLALCHEMY_DATABASE_URI')
    ECHO: bool                              = bool(int(os.getenv('ECHO')))
    SQLALCHEMY_TRACK_MODIFICATIONS: bool    = bool(int(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')))
    SESSION_COOKIE_SECURE: bool              = bool(int(os.getenv('SESSION_COOKIE_SECURE')))
    SESSION_COOKIE_HTTPONLY: bool           = bool(int(os.getenv('SESSION_COOKIE_HTTPONLY')))
    SESSION_COOKIE_SAMESITE: str            = os.getenv('SESSION_COOKIE_SAMESITE')
    PERMANENT_SESSION_LIFETIME: timedelta   = timedelta(seconds=int(os.getenv('PERMANENT_SESSION_LIFETIME')))
    FORCE_HTTPS: bool                       = bool(int(os.getenv('FORCE_HTTPS')))


@dataclass
class DevConfig:
    debug: bool     = False
    host: str       = "127.0.0.1"
    port: int       = 5000

    def __post_init__(self) -> None:
        config_file = Path(__file__).parent.parent / "app.dev.toml"
        try:
            cfg = load(config_file.open("rb"))
            self.debug   = cfg.get("DEBUG", False)
            self.host    = cfg.get("HOST", "127.0.0.1")
            self.port    = cfg.get("PORT", 5000)
        except FileNotFoundError: ...