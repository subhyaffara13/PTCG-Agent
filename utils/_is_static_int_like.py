
def _is_static_int_like(i):
    return (
        isinstance(i, int) and not ShapedType.is_dynamic_size(i)
    ) or _is_constant_int_like(i)

