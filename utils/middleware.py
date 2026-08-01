
def middleware(f: _Func) -> _Func:
    f.__middleware_version__ = 1  # type: ignore[attr-defined]
    return f

