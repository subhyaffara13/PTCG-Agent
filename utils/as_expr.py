
def as_expr(obj):
    """Convert non-Expr objects to Expr objects.
    """
    if isinstance(obj, complex):
        return as_complex(obj.real, obj.imag)
    if isinstance(obj, number_types):
        return as_number(obj)
    if isinstance(obj, str):
        # STRING expression holds string with boundary quotes, hence
        # applying repr:
        return as_string(repr(obj))
    if isinstance(obj, tuple):
        return tuple(map(as_expr, obj))
    return obj

