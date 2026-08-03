from typing import Any

def int_enum_validator(v: Any) -> IntEnum:
    if isinstance(v, IntEnum):
        return v

    raise errors.IntEnumError(value=v)

