from typing import Optional, List
from pydantic import BaseModel, condecimal
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
    item: str
    owner: str


class BookkeepingUpdate(BookkeepingBase):
    pass


class BookkeepingCreate(BookkeepingBase):
    pass


class Bookkeeping(BookkeepingBase):
    id: int
    data_created_at: Optional[DateTimeFmt] = None
    data_updated_at: Optional[DateTimeFmt] = None

    class Config:
        orm_mode = True


class BookkeepingList(BaseModel):
    data: Optional[List[Bookkeeping]] = []
    total: Optional[int] = 0
