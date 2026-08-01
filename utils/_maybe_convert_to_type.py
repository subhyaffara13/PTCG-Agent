
def _maybe_convert_to_type(a: NumberType, typ: type) -> NumberType:
    if not isinstance(a, Number):
        msg = f"Found unknown type {type(a)} when trying to convert scalars!"
        raise ValueError(msg)
    if not utils.is_weakly_lesser_type(type(a), typ):
        msg = f"Scalar {a} of type {type(a)} cannot be safely cast to type {typ}!"
        raise ValueError(msg)

    return typ(a)

