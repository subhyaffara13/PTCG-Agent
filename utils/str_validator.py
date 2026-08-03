from typing import Any, Union

def str_validator(v: Any) -> Union[str]:
    if isinstance(v, str):
        if isinstance(v, Enum):
            return v.value
        else:
            return v
    elif isinstance(v, (float, int, Decimal)):
        # is there anything else we want to add here? If you think so, create an issue.
        return str(v)
    elif isinstance(v, (bytes, bytearray)):
        return v.decode()
    else:
        raise errors.StrError()

