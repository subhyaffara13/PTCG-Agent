
def _require(x: _T | None, msg: str) -> _T:
    if x is None:
        raise RuntimeError(msg)
    return x

