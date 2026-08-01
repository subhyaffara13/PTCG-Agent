
def _is_none(x: Any) -> bool:
    return x is None or (x.node().mustBeNone() if isinstance(x, _C.Value) else False)

