# -*- coding: utf-8 -*-
from app.schemas import BookkeepingCreate, BookkeepingUpdate
from sqlalchemy.orm import Session
from ..models import Bookkeeping
from .base import CRUDBase


class CRUDBookkeeping(CRUDBase[Bookkeeping, BookkeepingCreate, BookkeepingUpdate]):
    def summary(self, db: Session, *, filter):
        total = super().get(db,
                            filter=filter,
                            select_alias={'total': 'sum(amount)'},
                            )
        data = super().query(db,
                             filter=filter,
                             select=['owner', 'item'],
                             select_alias={'total': 'sum(amount)'},
                             order_by='total desc',
                             group_by='bookkeeping_owner,bookkeeping_item',
                             limit=5
                             )
        trend = super().query(db,
                              filter=filter,
                              select=['month'],
                              select_alias={'total': 'sum(amount)'},
                              order_by='month asc',
                              group_by='month',
                              limit=50
                              )
        return {'total': total, 'data': data, 'trend': trend}


bookkeeping = CRUDBookkeeping(Bookkeeping)
