
def evalf_piecewise(expr: Expr, prec: int, options: OPT_DICT) -> TMP_RES:
    from .numbers import Float, Integer
    if 'subs' in options:
        expr = expr.subs(evalf_subs(prec, options['subs']))
        newopts = options.copy()
        del newopts['subs']
        if hasattr(expr, 'func'):
            return evalf(expr, prec, newopts)
        if isinstance(expr, float):
            return evalf(Float(expr), prec, newopts)
        if isinstance(expr, int):
            return evalf(Integer(expr), prec, newopts)

    # We still have undefined symbols
    raise NotImplementedError

