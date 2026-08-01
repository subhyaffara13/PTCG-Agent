
def eval_sum_direct(expr, limits):
    """
    Evaluate expression directly, but perform some simple checks first
    to possibly result in a smaller expression and faster execution.
    """
    (i, a, b) = limits

    dif = b - a
    # Linearity
    if expr.is_Mul:
        # Try factor out everything not including i
        without_i, with_i = expr.as_independent(i)
        if without_i != 1:
            s = eval_sum_direct(with_i, (i, a, b))
            if s:
                r = without_i*s
                if r is not S.NaN:
                    return r
        else:
            # Try term by term
            L, R = expr.as_two_terms()

            if not L.has(i):
                sR = eval_sum_direct(R, (i, a, b))
                if sR:
                    return L*sR

            if not R.has(i):
                sL = eval_sum_direct(L, (i, a, b))
                if sL:
                    return sL*R

    # do this whether its an Add or Mul
    # e.g. apart(1/(25*i**2 + 45*i + 14)) and
    # apart(1/((5*i + 2)*(5*i + 7))) ->
    # -1/(5*(5*i + 7)) + 1/(5*(5*i + 2))
    try:
        expr = apart(expr, i)  # see if it becomes an Add
    except PolynomialError:
        pass

    if expr.is_Add:
        # Try factor out everything not including i
        without_i, with_i = expr.as_independent(i)
        if without_i != 0:
            s = eval_sum_direct(with_i, (i, a, b))
            if s:
                r = without_i*(dif + 1) + s
                if r is not S.NaN:
                    return r
        else:
            # Try term by term
            L, R = expr.as_two_terms()
            lsum = eval_sum_direct(L, (i, a, b))
            rsum = eval_sum_direct(R, (i, a, b))

            if None not in (lsum, rsum):
                r = lsum + rsum
                if r is not S.NaN:
                    return r

    return Add(*[expr.subs(i, a + j) for j in range(dif + 1)])

