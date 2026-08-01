
def bool_validator(v: Any) -> bool:
    if v is True or v is False:
        return v
    if isinstance(v, bytes):
        v = v.decode()
    if isinstance(v, str):
        v = v.lower()
    try:
        if v in BOOL_TRUE:
            return True
        if v in BOOL_FALSE:
            return False
    except TypeError:
        raise errors.BoolError()
    raise errors.BoolError()

