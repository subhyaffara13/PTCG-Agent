
def _atleast_float_1(a):
    if not (a.dtype.is_floating_point or a.dtype.is_complex):
        a = a.to(_dtypes_impl.default_dtypes().float_dtype)
    return a

