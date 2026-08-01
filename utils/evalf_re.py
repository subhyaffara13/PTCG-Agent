
def evalf_re(expr: 're', prec: int, options: OPT_DICT) -> TMP_RES:
    return get_complex_part(expr.args[0], 0, prec, options)

