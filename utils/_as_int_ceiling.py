
def _as_int_ceiling(a):
    """ Wrapping ceiling in as_int will raise an error if there was a problem
        determining whether the expression was exactly an integer or not."""
    from sympy.functions.elementary.integers import ceiling
    return as_int(ceiling(a))

