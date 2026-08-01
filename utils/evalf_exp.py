
def evalf_exp(expr: 'exp', prec: int, options: OPT_DICT) -> TMP_RES:
    from .power import Pow
    return evalf_pow(Pow(S.Exp1, expr.exp, evaluate=False), prec, options)

