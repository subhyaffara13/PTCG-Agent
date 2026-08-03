from typing import Any, Union

def strict_str_validator(v: Any) -> Union[str]:
    if isinstance(v, str) and not isinstance(v, Enum):
        return v
    raise errors.StrError()

