# -*- coding: utf-8 -*-
import os
import sys
from functools import lru_cache
from pydantic import BaseSettings

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class Settings(BaseSettings):
    FASTAPI_CONFIG: str = 'development'
    APP_NAME: str = "Mblocks Bookkeeping"
    OPENAPI_PREFIX: str = ""
    SQLALCHEMY_DATABASE_URI: str = prefix + os.path.join(basedir, 'data.db')
    SQLALCHEMY_ECHO: bool = True

    class Config:
        case_sensitive: bool = True
        env_file: bool = ".env"


class Production(Settings):
    SQLALCHEMY_DATABASE_URI: str = 'sqlite://///data/data.db'
    SQLALCHEMY_ECHO: bool = False

class Test(Settings):
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///test.db'


@lru_cache()
def get_settings():
    if os.getenv("FASTAPI_CONFIG") == 'test':
        return Test()
    if os.getenv("FASTAPI_CONFIG") == 'production':
        return Production()
    return Settings()
