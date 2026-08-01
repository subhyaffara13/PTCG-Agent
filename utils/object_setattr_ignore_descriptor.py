
def object_setattr_ignore_descriptor(obj: Any, name: str, value: Any) -> None:
    # https://github.com/python/cpython/blob/3.11/Objects/object.c#L1286-L1335
    d = object.__getattribute__(obj, "__dict__")
    d[name] = value

