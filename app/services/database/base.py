from sqlalchemy import Boolean, Column, Integer, BigInteger, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, index=True, autoincrement=True)
    __name__: str
    # Generate __tablename__ automatically

    data_enabled = Column(Boolean, default=True)
    data_created_at = Column(DateTime, server_default=func.now())
    data_updated_at = Column(DateTime,onupdate=func.now())
    data_deleted_at = Column(DateTime)
    data_created_by = Column(BigInteger)
    data_updated_by = Column(BigInteger)
    data_deleted_by = Column(BigInteger)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
