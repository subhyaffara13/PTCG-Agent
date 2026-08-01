
def evalf_integer(expr: 'Integer', prec: int, options: OPT_DICT) -> TMP_RES:
    return from_int(expr.p, prec), None, prec, None

