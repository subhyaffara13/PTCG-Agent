
def _real_to_rational(expr, tolerance=None, rational_conversion='base10'):
    """
    Replace all reals in expr with rationals.

    Examples
    ========

    >>> from sympy.simplify.simplify import _real_to_rational
    >>> from sympy.abc import x

    >>> _real_to_rational(.76 + .1*x**.5)
    sqrt(x)/10 + 19/25

    If rational_conversion='base10', this uses the base-10 string. If
    rational_conversion='exact', the exact, base-2 representation is used.

    >>> _real_to_rational(0.333333333333333, rational_conversion='exact')
    6004799503160655/18014398509481984
    >>> _real_to_rational(0.333333333333333)
    1/3

    """
    expr = _sympify(expr)
    inf = Float('inf')
    p = expr
    reps = {}
    reduce_num = None
    if tolerance is not None and tolerance < 1:
        reduce_num = ceiling(1/tolerance)
    for fl in p.atoms(Float):
        key = fl
        if reduce_num is not None:
            r = Rational(fl).limit_denominator(reduce_num)
        elif (tolerance is not None and tolerance >= 1 and
                fl.is_Integer is False):
            r = Rational(tolerance*round(fl/tolerance)
                ).limit_denominator(int(tolerance))
        else:
            if rational_conversion == 'exact':
                r = Rational(fl)
                reps[key] = r
                continue
            elif rational_conversion != 'base10':
                raise ValueError("rational_conversion must be 'base10' or 'exact'")

            r = nsimplify(fl, rational=False)
            # e.g. log(3).n() -> log(3) instead of a Rational
            if fl and not r:
                r = Rational(fl)
            elif not r.is_Rational:
                if fl in (inf, -inf):
                    r = S.ComplexInfinity
                elif fl < 0:
                    fl = -fl
                    d = Pow(10, int(mpmath.log(fl)/mpmath.log(10)))
                    r = -Rational(str(fl/d))*d
                elif fl > 0:
                    d = Pow(10, int(mpmath.log(fl)/mpmath.log(10)))
                    r = Rational(str(fl/d))*d
                else:
                    r = S.Zero
        reps[key] = r
    return p.subs(reps, simultaneous=True)

