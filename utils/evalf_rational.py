
def evalf_rational(expr: 'Rational', prec: int, options: OPT_DICT) -> TMP_RES:
    return from_rational(expr.p, expr.q, prec), None, prec, None

