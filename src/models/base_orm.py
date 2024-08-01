from typing import Type

from sqlalchemy.orm import DeclarativeBase

from .base_dto import BaseDTO


class BaseORM(DeclarativeBase):
    __dto__: Type[BaseDTO] = None

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
