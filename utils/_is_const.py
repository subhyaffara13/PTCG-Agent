
def _is_const(value) -> bool:
    return isinstance(value, tuple(CONST_CLS))

