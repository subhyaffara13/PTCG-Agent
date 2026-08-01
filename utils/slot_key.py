
def slot_key(attr: str) -> str:
    """Map dunder method name to sort key.

    Sort reverse operator methods and __delitem__ after others ('x' > '_').
    """
    if (attr.startswith("__r") and attr != "__rshift__") or attr == "__delitem__":
        return "x" + attr
    return attr

