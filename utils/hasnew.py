
def hasnew(obj: object) -> bool:
    new: object = getattr(obj, "__new__", None)
    if new:
        return new != object.__new__
    return False

