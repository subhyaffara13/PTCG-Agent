
def hasinit(obj: object) -> bool:
    init: object = getattr(obj, "__init__", None)
    if init:
        return init != object.__init__
    return False

