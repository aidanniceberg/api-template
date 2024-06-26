import logging
from typing import Any, ClassVar, List, Optional, Type

from sqlalchemy import ColumnElement, delete, insert, select, update
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session

from ..models.base_dto import BaseDTO
from ..models.base_orm import BaseORM
from .utils import errorhandle

logger = logging.getLogger(__name__)


class BaseDAO:
    __orm_model__: ClassVar[Type[BaseORM]] = None

    @classmethod
    @errorhandle(logger)
    def insert(cls, session: Session, dto: BaseDTO):
        """
        Insert a record into the database
        :param session: database session
        :param dto: entity to insert
        :return: inserted entity
        """
        orm = cls.__orm_model__.from_dto(dto)
        session.add(orm)
        session.commit()
        return orm.to_dto()

    @classmethod
    @errorhandle(logger)
    def insertmany(cls, session: Session, dtos: List[BaseDTO]):
        """
        Insert multiple records into the database
        :param session: database session
        :param dtos: list of entities to insert
        :return: inserted entities
        """
        stmt = insert(cls.__orm_model__).returning(cls.__orm_model__)
        orm_models = [cls.__orm_model__.from_dto(dto) for dto in dtos]
        results = session.scalars(stmt, orm_models)
        return [result.to_dto() for result in results]

    @classmethod
    @errorhandle(logger)
    def fetchone(cls, session: Session, **kwargs):
        """
        Fetch one record from the database
        :param session: database session
        :param kwargs: filter args
        :return: fetched record, or None if it doesn't exist
        """
        stmt = select(cls.__orm_model__).filter_by(**kwargs)
        result = session.scalars(stmt).one_or_none()
        return result.to_dto() if result else None

    @classmethod
    @errorhandle(logger)
    def fetchall(
        cls,
        session: Session,
        order_by: Optional[ColumnElement] = None,
        desc: bool = True,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **kwargs,
    ):
        """
        :param session: database session
        :param order_by: column to order by
        :param desc: order descending
        :param limit: max records to return
        :param offset: offset of records to return
        :param kwargs: filter args
        :return: fetched entities
        """
        stmt = select(cls.__orm_model__).filter_by(**kwargs)
        if order_by:
            order_by = order_by.desc() if desc else order_by.asc()
            stmt = stmt.order_by(order_by)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        results = session.scalars(stmt).all()
        return [result.to_dto() for result in results]

    @classmethod
    @errorhandle(logger)
    def fetchfirst(
        cls,
        session: Session = None,
        order_by: Optional[ColumnElement] = None,
        desc: bool = True,
        **kwargs,
    ):
        """
        Fetch first record from the database
        :param session: database session
        :param order_by: column to order by
        :param desc: order descending
        :param kwargs: filter args
        :return: fetched entity if exists else None
        """
        stmt = select(cls.__orm_model__).filter_by(**kwargs)
        if order_by:
            order_by = order_by.desc() if desc else order_by.asc()
            stmt = stmt.order_by(order_by)
        result = session.scalar(stmt)
        return result.to_dto() if result else None

    @classmethod
    @errorhandle(logger)
    def delete(cls, session: Session, pkey: Any, orm_model: Type[BaseORM] = None):
        """
        Delete a record from the database
        :param session: database session
        :param pkey: primary key to search for
        :param orm_model: model to delete. If None, defaults to cls.__orm_model__
        :return: deleted entity
        """
        orm_model = orm_model or cls.__orm_model__
        pkey_cols = inspect(orm_model).primary_key
        assert pkey_cols, f"{orm_model} does not have any primary keys"
        pkey_col = pkey_cols[0]
        stmt = delete(orm_model).where(pkey_col == pkey).returning(orm_model)
        result = session.scalars(stmt).one()
        result_dto = result.to_dto()
        return result_dto

    @classmethod
    @errorhandle(logger)
    def update(
        cls, session: Session, pkey: Any, orm_model: Type[BaseORM] = None, **kwargs
    ):
        """
        Updates a record from the database
        :param session: database session
        :param pkey: primary key to search for
        :param orm_model: model to delete. If None, defaults to cls.__orm_model__
        :param kwargs: args to update
        :return: deleted entity
        """
        orm_model = orm_model or cls.__orm_model__
        pkey_cols = inspect(orm_model).primary_key
        assert pkey_cols, f"{orm_model} does not have any primary keys"
        pkey_col = pkey_cols[0]
        stmt = (
            update(orm_model)
            .where(pkey_col == pkey)
            .values(kwargs)
            .returning(orm_model)
        )
        result = session.scalars(stmt).one()
        return result.to_dto()
