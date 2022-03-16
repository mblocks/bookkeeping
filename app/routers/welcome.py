# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app import schemas
from app.services import database
from app.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=schemas.BookkeepingList)
async def query(db: Session = Depends(database.client),
                current_user: schemas.CurrentUser = Depends(get_current_user),
                page: int = Query(1, ge=1),
                page_size: int = Query(10, ge=1, le=100),
                total: int = None
                ):
    """
        Query bookkeeping
    """
    filter = {'data_created_by': current_user.id}
    skip = (page - 1) * page_size
    limit = page_size
    data = database.crud.bookkeeping.query(db, filter=filter, skip=skip, limit=limit)  # nopep8
    if not total:
        total = database.crud.bookkeeping.count(db, filter=filter)
    return {'total': total, 'data': data}


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
