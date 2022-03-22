from typing import Optional, List
from enum import Enum
from unicodedata import category
from pydantic import BaseModel, condecimal, root_validator
from datetime import date, datetime


class DateTimeFmt(datetime):
    @classmethod
    def __get_validators__(cls):
        # https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, datetime):
            return v.strftime('%Y-%m-%d %H:%M')
        return v

    def __repr__(self):
        return f'DateTimeFmt({super().__repr__()})'


class BookkeepingBase(BaseModel):
    type: str
    trade_at: Optional[date] = None
    amount: condecimal(decimal_places=2)
    category: Optional[str] = None
    item: str
    owner: str


class BookkeepingUpdate(BookkeepingBase):
    pass


class BookkeepingCreate(BookkeepingUpdate):
    pass


class BookkeepingImport(BookkeepingUpdate):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Bookkeeping(BookkeepingBase):
    id: int
    month: Optional[str] = None
    data_created_at: Optional[DateTimeFmt] = None
    data_updated_at: Optional[DateTimeFmt] = None

    class Config:
        orm_mode = True


class BookkeepingList(BaseModel):
    data: Optional[List[Bookkeeping]] = []
    total: Optional[int] = 0


class BookkeepingStatistics(str, Enum):
    owner = "owner"
    item = "item"
    category = "category"
