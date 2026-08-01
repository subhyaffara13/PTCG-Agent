
def int_validator(v: Any) -> int:
    if isinstance(v, int) and not (v is True or v is False):
        return v

    # see https://github.com/pydantic/pydantic/issues/1477 and in turn, https://github.com/python/cpython/issues/95778
    # this check should be unnecessary once patch releases are out for 3.7, 3.8, 3.9 and 3.10
    # but better to check here until then.
    # NOTICE: this does not fully protect user from the DOS risk since the standard library JSON implementation
    # (and other std lib modules like xml) use `int()` and are likely called before this, the best workaround is to
    # 1. update to the latest patch release of python once released, 2. use a different JSON library like ujson
    if isinstance(v, (str, bytes, bytearray)) and len(v) > max_str_int:
        raise errors.IntegerError()

    try:
        return int(v)
    except (TypeError, ValueError, OverflowError):
        raise errors.IntegerError()

