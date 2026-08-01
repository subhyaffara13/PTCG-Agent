
def _value_or(opt: T | None, default: T) -> T:
    return opt if opt is not None else default

