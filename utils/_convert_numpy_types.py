
def _convert_numpy_types(a, **sympify_args):
    """
    Converts a numpy datatype input to an appropriate SymPy type.
    """
    import numpy as np
    if not isinstance(a, np.floating):
        if np.iscomplex(a):
            return _sympy_converter[complex](a.item())
        else:
            return sympify(a.item(), **sympify_args)
    else:
        from .numbers import Float
        prec = np.finfo(a).nmant + 1
        # E.g. double precision means prec=53 but nmant=52
        # Leading bit of mantissa is always 1, so is not stored
        if np.isposinf(a):
            return Float('inf')
        elif np.isneginf(a):
            return Float('-inf')
        else:
            p, q = a.as_integer_ratio()
            a = mlib.from_rational(p, q, prec)
            return Float(a, precision=prec)

