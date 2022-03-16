# -*- coding: utf-8 -*-
from app.schemas import BookkeepingCreate, BookkeepingUpdate
from ..models import Bookkeeping
from .base import CRUDBase


class CRUDBookkeeping(CRUDBase[Bookkeeping, BookkeepingCreate, BookkeepingUpdate]):
    pass


bookkeeping = CRUDBookkeeping(Bookkeeping)
