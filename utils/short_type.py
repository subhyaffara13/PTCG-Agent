
def short_type(obj: object) -> str:
    """Return the last component of the type name of an object.

    If obj is None, return 'nil'. For example, if obj is 1, return 'int'.
    """
    if obj is None:
        return "nil"
    t = str(type(obj))
    return t.split(".")[-1].rstrip("'>")

