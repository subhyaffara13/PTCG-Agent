
def evalf_floor(expr: 'floor', prec: int, options: OPT_DICT) -> TMP_RES:
    return get_integer_part(expr.args[0], -1, options)

