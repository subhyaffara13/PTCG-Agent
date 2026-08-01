
def rewrite_module(obj: _T) -> _T:
    obj.__module__ = "yarl"
    return obj

