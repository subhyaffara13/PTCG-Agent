
def _mk_defaulter(d: T) -> Callable[[T | None], T]:
    return lambda x: x if x is not None else d

