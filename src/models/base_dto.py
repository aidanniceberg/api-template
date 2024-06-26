from dataclasses import Field, dataclass, fields


@dataclass
class BaseDTO:
    @classmethod
    def fields(cls) -> tuple[Field, ...]:
        return fields(cls)
