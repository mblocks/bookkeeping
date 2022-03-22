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
                             select=['owner', 'category'],
                             select_alias={'amount': 'sum(amount)'},
                             order_by='amount desc',
                             group_by='bookkeeping_owner,bookkeeping_category',
                             limit=5
                             )
        trend = super().query(db,
                              filter=filter,
                              select=['month'],
                              select_alias={'amount': 'sum(amount)'},
                              order_by='month asc',
                              group_by='month',
                              limit=50
                              )
        return {'total': total.total, 'data': data, 'trend': trend}

    def batch(self, db: Session, *, data, filter):
        inserted = 0
        updated = 0
        for item in data:
            if item.id:
                super().update(db, filter={**filter,'id':item.id}, payload=item, commit=False, refresh=False)
                updated += 1
            else:
                super().create(db=db, payload={**item.dict(exclude_unset=True),**filter}, commit=False, refresh=False)
                inserted += 1
        db.commit()
        return {'result':True, 'inserted': inserted, 'updated': updated}

bookkeeping = CRUDBookkeeping(Bookkeeping)
