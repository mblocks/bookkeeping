# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING
from sqlalchemy import Column, String, DateTime, DECIMAL, Float
from app.services.database.base import Base


class Bookkeeping(Base):
    __tablename__ = "bookkeeping"
    type = Column(String(10))
    trade_at = Column(DateTime().with_variant(String(10), "sqlite"))
    month = Column(String(10))
    amount = Column(DECIMAL(scale=2).with_variant(Float, "sqlite"))
    item = Column(String(100))
    owner = Column("owner", String(100))
