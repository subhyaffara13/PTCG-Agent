
def piecewise_simplify(expr, **kwargs):
    expr = piecewise_simplify_arguments(expr, **kwargs)
    if not isinstance(expr, Piecewise):
        return expr
    args = list(expr.args)

    args = _piecewise_simplify_eq_and(args)
    args = _piecewise_simplify_equal_to_next_segment(args)
    return Piecewise(*args)

