
def istestfunc(func) -> bool:
    return callable(func) and getattr(func, "__name__", "<lambda>") != "<lambda>"

