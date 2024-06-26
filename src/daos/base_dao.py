import logging
from typing import List, Any, Type, ClassVar, Optional

from sqlalchemy import delete, select, update, ColumnElement, insert
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session

from .utils import errorhandle
from ..models.base_dto import BaseDTO
from ..models.base_orm import BaseORM

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
        session.commit()
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
    def delete(cls, session: Session, pkey: Any):
        """
        Delete a record from the database
        :param session: database session
        :param pkey: primary key to search for
        :return: deleted entity
        """
        pkey_cols = inspect(cls.__orm_model__).primary_key
        assert pkey_cols, f"{cls.__orm_model__} does not have any primary keys"
        pkey_col = pkey_cols[0]
        stmt = (
            delete(cls.__orm_model__)
            .where(pkey_col == pkey)
            .returning(cls.__orm_model__)
        )
        result = session.scalars(stmt).one()
        session.commit()
        return result.to_dto()

    @classmethod
    @errorhandle(logger)
    def update(cls, session: Session, pkey: Any, **kwargs):
        """
        Updates a record from the database
        :param session: database session
        :param pkey: primary key to search for
        :param kwargs: args to update
        :return: deleted entity
        """
        pkey_cols = inspect(cls.__orm_model__).primary_key
        assert pkey_cols, f"{cls.__orm_model__} does not have any primary keys"
        pkey_col = pkey_cols[0]
        stmt = (
            update(cls.__orm_model__)
            .where(pkey_col == pkey)
            .values(kwargs)
            .returning(cls.__orm_model__)
        )
        result = session.scalars(stmt).one()
        session.commit()
        return result.to_dto()
