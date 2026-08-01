
def value_borrow_scope(builder: IRBuilder, v: Value) -> int:
    """Compute how long an existing borrowed value can safely be kept alive.

    Returns a KEEP_ALIVE_* constant (or a large value if 'v' is not borrowed and
    thus has no borrowing constraint).
    """
    if isinstance(v, GetAttr) and v.is_borrowed:
        return min(v.borrow_scope, value_borrow_scope(builder, v.obj))
    elif isinstance(v, Cast) and v.is_borrowed:
        # A cast just propagates the value (when successful), so the scope is
        # determined by the source.
        return value_borrow_scope(builder, v.src)
    elif isinstance(v, (CallC, PrimitiveOp)) and v.is_borrowed:
        # Values borrowed from a C function (e.g. a borrowed list/vec item) may be
        # invalidated by arbitrary computation, so they are only short-lived.
        return KEEP_ALIVE_SHORT_LIVED
    return 999

