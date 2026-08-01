
def _RealPredicate_number(expr, assumptions):
    # let as_real_imag() work first since the expression may
    # be simpler to evaluate
    i = expr.as_real_imag()[1].evalf(2)
    if i._prec != 1:
        return not i

