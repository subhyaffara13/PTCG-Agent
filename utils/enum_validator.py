from typing import Any

def enum_validator(v: Any) -> Enum:
    if isinstance(v, Enum):
        return v

    raise errors.EnumError(value=v)

