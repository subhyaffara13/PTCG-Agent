
def _extract_python_literal(value: Value) -> object:
    if isinstance(value, Integer):
        if is_none_rprimitive(value.type):
            return None
        val = value.numeric_value()
        if is_bool_rprimitive(value.type):
            return bool(val)
        return val
    elif isinstance(value, Float):
        return value.value
    elif isinstance(value, LoadLiteral):
        return value.value
    elif isinstance(value, Box):
        return _extract_python_literal(value.src)
    elif isinstance(value, TupleSet):
        items = tuple(_extract_python_literal(item) for item in value.items)
        if any(itm is _NOT_REPRESENTABLE for itm in items):
            return _NOT_REPRESENTABLE
        return items
    return _NOT_REPRESENTABLE

