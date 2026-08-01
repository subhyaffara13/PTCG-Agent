
def evalf_alg_num(a: 'AlgebraicNumber', prec: int, options: OPT_DICT) -> TMP_RES:
    return evalf(a.to_root(), prec, options)

