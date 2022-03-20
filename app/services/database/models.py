# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING
from sqlalchemy import Column, String, DateTime, DECIMAL, Float
from sqlalchemy.ext.hybrid import hybrid_property
from app.services.database.base import Base


class Bookkeeping(Base):
    __tablename__ = "bookkeeping"
    type = Column(String(10))
    _trade_at = Column('trade_at', DateTime().with_variant(String(10), "sqlite"))  # nopep8
    month = Column(String(10))
    amount = Column(DECIMAL(scale=2).with_variant(Float, "sqlite"))
    item = Column(String(100))
    owner = Column("owner", String(100))

    @hybrid_property
    def trade_at(self):
        return self._trade_at

    @trade_at.setter
    def trade_at(self, value):
        self.month = value[:7] if type(value) == str else value.strftime("%Y-%m")  # nopep8
        self._trade_at = value
