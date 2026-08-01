
def get_complex_part(expr: Expr, no: int, prec: int, options: OPT_DICT) -> TMP_RES:
    """no = 0 for real part, no = 1 for imaginary part"""
    workprec = prec
    i = 0
    while 1:
        res = evalf(expr, workprec, options)
        if res is S.ComplexInfinity:
            return fnan, None, prec, None
        value, accuracy = res[no::2]
        # XXX is the last one correct? Consider re((1+I)**2).n()
        if (not value) or accuracy >= prec or -value[2] > prec:
            return value, None, accuracy, None
        workprec += max(30, 2**i)
        i += 1

