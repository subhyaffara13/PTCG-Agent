
def meijerint_definite(f, x, a, b):
    """
    Integrate ``f`` over the interval [``a``, ``b``], by rewriting it as a product
    of two G functions, or as a single G function.

    Return res, cond, where cond are convergence conditions.

    Examples
    ========

    >>> from sympy.integrals.meijerint import meijerint_definite
    >>> from sympy import exp, oo
    >>> from sympy.abc import x
    >>> meijerint_definite(exp(-x**2), x, -oo, oo)
    (sqrt(pi), True)

    This function is implemented as a succession of functions
    meijerint_definite, _meijerint_definite_2, _meijerint_definite_3,
    _meijerint_definite_4. Each function in the list calls the next one
    (presumably) several times. This means that calling meijerint_definite
    can be very costly.
    """
    # This consists of three steps:
    # 1) Change the integration limits to 0, oo
    # 2) Rewrite in terms of G functions
    # 3) Evaluate the integral
    #
    # There are usually several ways of doing this, and we want to try all.
    # This function does (1), calls _meijerint_definite_2 for step (2).
    _debugf('Integrating %s wrt %s from %s to %s.', (f, x, a, b))
    f = sympify(f)
    if f.has(DiracDelta):
        _debug('Integrand has DiracDelta terms - giving up.')
        return None

    if f.has(SingularityFunction):
        _debug('Integrand has Singularity Function terms - giving up.')
        return None

    f_, x_, a_, b_ = f, x, a, b

    # Let's use a dummy in case any of the boundaries has x.
    d = Dummy('x')
    f = f.subs(x, d)
    x = d

    if a == b:
        return (S.Zero, True)

    results = []
    if a is S.NegativeInfinity and b is not S.Infinity:
        return meijerint_definite(f.subs(x, -x), x, -b, -a)

    elif a is S.NegativeInfinity:
        # Integrating -oo to oo. We need to find a place to split the integral.
        _debug('  Integrating -oo to +oo.')
        innermost = _find_splitting_points(f, x)
        _debug('  Sensible splitting points:', innermost)
        for c in sorted(innermost, key=default_sort_key, reverse=True) + [S.Zero]:
            _debug('  Trying to split at', c)
            if not c.is_extended_real:
                _debug('  Non-real splitting point.')
                continue
            res1 = _meijerint_definite_2(f.subs(x, x + c), x)
            if res1 is None:
                _debug('  But could not compute first integral.')
                continue
            res2 = _meijerint_definite_2(f.subs(x, c - x), x)
            if res2 is None:
                _debug('  But could not compute second integral.')
                continue
            res1, cond1 = res1
            res2, cond2 = res2
            cond = _condsimp(And(cond1, cond2))
            if cond == False:
                _debug('  But combined condition is always false.')
                continue
            res = res1 + res2
            return res, cond

    elif a is S.Infinity:
        res = meijerint_definite(f, x, b, S.Infinity)
        return -res[0], res[1]

    elif (a, b) == (S.Zero, S.Infinity):
        # This is a common case - try it directly first.
        res = _meijerint_definite_2(f, x)
        if res:
            if _has(res[0], meijerg):
                results.append(res)
            else:
                return res

    else:
        if b is S.Infinity:
            for split in _find_splitting_points(f, x):
                if (a - split >= 0) == True:
                    _debugf('Trying x -> x + %s', split)
                    res = _meijerint_definite_2(f.subs(x, x + split)
                                                *Heaviside(x + split - a), x)
                    if res:
                        if _has(res[0], meijerg):
                            results.append(res)
                        else:
                            return res

        f = f.subs(x, x + a)
        b = b - a
        a = 0
        if b is not S.Infinity:
            phi = exp(S.ImaginaryUnit*arg(b))
            b = Abs(b)
            f = f.subs(x, phi*x)
            f *= Heaviside(b - x)*phi
            b = S.Infinity

        _debug('Changed limits to', a, b)
        _debug('Changed function to', f)
        res = _meijerint_definite_2(f, x)
        if res:
            if _has(res[0], meijerg):
                results.append(res)
            else:
                return res
    if f_.has(HyperbolicFunction):
        _debug('Try rewriting hyperbolics in terms of exp.')
        rv = meijerint_definite(
            _rewrite_hyperbolics_as_exp(f_), x_, a_, b_)
        if rv:
            if not isinstance(rv, list):
                from sympy.simplify.radsimp import collect
                rv = (collect(factor_terms(rv[0]), rv[0].atoms(exp)),) + rv[1:]
                return rv
            results.extend(rv)
    if results:
        return next(ordered(results))

