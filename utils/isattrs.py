
def isattrs(obj: object) -> bool:
    return getattr(obj, "__attrs_attrs__", None) is not None

