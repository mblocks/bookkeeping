# -*- coding: utf-8 -*-
from fastapi import FastAPI
from . import routers

app = FastAPI()

app.include_router(routers.welcome, tags=["welcome"])

