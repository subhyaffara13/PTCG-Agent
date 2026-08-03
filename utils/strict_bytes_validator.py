from typing import Any, Union

def strict_bytes_validator(v: Any) -> Union[bytes]:
    if isinstance(v, bytes):
        return v
    elif isinstance(v, bytearray):
        return bytes(v)
    else:
        raise errors.BytesError()

