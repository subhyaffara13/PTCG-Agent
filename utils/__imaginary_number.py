
def _Imaginary_number(expr, assumptions):
    # let as_real_imag() work first since the expression may
    # be simpler to evaluate
    r = expr.as_real_imag()[0].evalf(2)
    if r._prec != 1:
        return not r

