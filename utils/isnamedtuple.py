
def isnamedtuple(obj: object) -> bool:
    return isinstance(obj, tuple) and getattr(obj, "_fields", None) is not None

