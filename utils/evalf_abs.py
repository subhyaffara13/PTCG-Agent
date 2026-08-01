
def evalf_abs(expr: 'Abs', prec: int, options: OPT_DICT) -> TMP_RES:
    return get_abs(expr.args[0], prec, options)

