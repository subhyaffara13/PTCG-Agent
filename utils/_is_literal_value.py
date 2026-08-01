
def _is_literal_value(obj: object) -> TypeGuard[LiteralValue]:
    return isinstance(obj, (str, bytes, int, float, complex, tuple, frozenset, type(None)))

