from typing import Type

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase

from .base_dto import BaseDTO


class BaseORM(DeclarativeBase):
    __dto__: Type[BaseDTO] = None

    @classmethod
    def from_dto(cls, dto: BaseDTO):
        attrs = dict()
        relationships = {rel.name: rel for rel in inspect(cls).relationships}
        for field in dto.fields():
            if hasattr(dto, field.name):
                if issubclass(field.type, BaseDTO):
                    orm_klass = relationships[field.name].class_
                    attr = getattr(dto, field.name)
                    attrs[field.name] = orm_klass.from_dto(attr) if attr else None
                else:
                    attrs[field.name] = getattr(dto, field.name)
        return cls(**attrs)

    def to_dto(self):
        if self.__dto__ is None:
            raise RuntimeError("__dto__ attribute must be set to call to_dto()")
        attrs = dict()
        for field in self.__dto__.fields():
            if hasattr(self, field.name):
                if issubclass(field.type, BaseDTO):
                    attr = getattr(self, field.name)
                    attrs[field.name] = attr.to_dto() if attr else None
                else:
                    attrs[field.name] = getattr(self, field.name)
        return self.__dto__(**attrs)
