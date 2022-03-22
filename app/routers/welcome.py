# -*- coding: utf-8 -*-
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, File, UploadFile
from sqlalchemy.orm import Session
from app import schemas
from app.services import database
from app.deps import get_current_user
from app.utils import xls_to_list, list_to_xls

router = APIRouter()


@router.get("/", response_model=schemas.BookkeepingList)
async def query(db: Session = Depends(database.client),
                current_user: schemas.CurrentUser = Depends(get_current_user),
                page: int = Query(1, ge=1),
                page_size: int = Query(10, ge=1, le=100),
                category: Optional[str] = None,
                item: Optional[str] = None,
                trade_start: Optional[str] = None,
                trade_end: Optional[str] = None,
                total: int = None
                ):
    """
        Query bookkeeping
    """
    filter = {'data_created_by': current_user.id, 'category': category, 'item': item, 'trade_at >=': trade_start, 'trade_at <=': trade_end}
    skip = (page - 1) * page_size
    limit = page_size
    data = database.crud.bookkeeping.query(db, filter=filter, skip=skip, limit=limit, order_by='trade_at desc')  # nopep8
    if not total:
        total = database.crud.bookkeeping.count(db, filter=filter)
    return {'total': total, 'data': data}


@router.get("/summary")
async def summary(db: Session = Depends(database.client),
                  current_user: schemas.CurrentUser = Depends(get_current_user)
                  ):
    """
        Query bookkeeping summary
    """
    filter = {'data_created_by': current_user.id}
    return database.crud.bookkeeping.summary(db, filter=filter)


@router.get("/statistics")
async def statistics(name: Optional[List[schemas.BookkeepingStatistics]] = Query(None),
                        db: Session = Depends(database.client),
                        current_user: schemas.CurrentUser = Depends(get_current_user),
                  ):
    """
        Query bookkeeping statistic
    """
    result = {}
    for i in name:
        items = database.crud.bookkeeping.query(db,
                                                filter={'data_created_by': current_user.id},
                                                select=[i.value],
                                                select_alias={'count':'count(*)'},
                                                group_by=i.value,
                                                order_by='count desc',
                                                )
        result[i.value] = [{'count':item.count,'name':getattr(item,i.value)} for item in items]
    return result


@router.get("/export")
async def export_excel(db: Session = Depends(database.client),
                       current_user: schemas.CurrentUser = Depends(get_current_user),
                       category: Optional[str] = None,
                       item: Optional[str] = None,
                       trade_start: Optional[str] = None,
                       trade_end: Optional[str] = None,
                       ):
    """
        Export bookkeeping data to excel
    """
    filter = {'data_created_by': current_user.id, 'category': category, 'item': item, 'trade_at >=': trade_start, 'trade_at <=': trade_end}
    columns = ['id', 'month', 'trade_at', 'type', 'category','item',
               'owner', 'amount', 'data_created_at', 'data_updated_at']
    data = database.crud.bookkeeping.query(db, select=columns, filter=filter, order_by='trade_at desc')
    return list_to_xls(name='bookkeepings.xls', columns=columns, data=data)


@router.post("/import")
async def import_excel(file: UploadFile = File(...),
                       db: Session = Depends(database.client),
                       current_user: schemas.CurrentUser = Depends(get_current_user),  # nopep8
                       ):
    """
        Import excel upadte bookkeeping
    """
    filter = {'data_created_by': current_user.id}
    columns = ['id', 'month', 'trade_at', 'type', 'category','item',
               'owner', 'amount', 'data_created_at', 'data_updated_at']
    result, data = xls_to_list(await file.read(), mapper={v: v for v in columns})
    schema_data = [schemas.BookkeepingImport(**item) for item in data]
    return database.crud.bookkeeping.batch(db, data=schema_data, filter=filter)


@router.post("/", response_model=schemas.Bookkeeping)
async def create(payload: schemas.BookkeepingCreate,
                 db: Session = Depends(database.client),
                 current_user: schemas.CurrentUser = Depends(get_current_user),
                 ):
    """
        Create bookkeeping
    """
    data = {**payload.dict(), 'data_created_by': current_user.id}
    created_bookkeeping = database.crud.bookkeeping.create(db, payload=data)
    return created_bookkeeping


@router.post("/{id}/delete", response_model=schemas.Bookkeeping)
async def delete(id: int,
                 db: Session = Depends(database.client),
                 current_user: schemas.CurrentUser = Depends(get_current_user),
                 ):
    filter = {'id': id, 'data_created_by': current_user.id}
    deleted_bookkeeping = database.crud.bookkeeping.get(db, filter=filter)
    database.crud.bookkeeping.delete(db, filter=filter)
    return deleted_bookkeeping


@router.post("/{id}", response_model=schemas.Bookkeeping)
async def update(id: int,
                 payload: schemas.BookkeepingUpdate,
                 db: Session = Depends(database.client),
                 current_user: schemas.CurrentUser = Depends(get_current_user)
                 ):
    filter = {'id': id, 'data_created_by': current_user.id}
    updated_bookkeeping = database.crud.bookkeeping.update(
        db, filter=filter, payload=payload)
    return updated_bookkeeping
