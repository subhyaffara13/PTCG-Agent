
def evalf_im(expr: 'im', prec: int, options: OPT_DICT) -> TMP_RES:
    return get_complex_part(expr.args[0], 1, prec, options)

