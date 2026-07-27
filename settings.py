import os
from typing import Optional


class Config:
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI: str | None = os.getenv(
        'DATABASE_URI',
        'sqlite:///db.sqlite3',
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DISK_TOKEN: Optional[str] = os.getenv('DISK_TOKEN')
