
def meijerint_inversion(f, x, t):
    r"""
    Compute the inverse laplace transform
    $\int_{c+i\infty}^{c-i\infty} f(x) e^{tx}\, dx$,
    for real c larger than the real part of all singularities of ``f``.

    Note that ``t`` is always assumed real and positive.

    Return None if the integral does not exist or could not be evaluated.

    Examples
    ========

    >>> from sympy.abc import x, t
    >>> from sympy.integrals.meijerint import meijerint_inversion
    >>> meijerint_inversion(1/x, x, t)
    Heaviside(t)
    """
    f_ = f
    t_ = t
    t = Dummy('t', polar=True)  # We don't want sqrt(t**2) = abs(t) etc
    f = f.subs(t_, t)
    _debug('Laplace-inverting', f)
    if not _is_analytic(f, x):
        _debug('But expression is not analytic.')
        return None
    # Exponentials correspond to shifts; we filter them out and then
    # shift the result later.  If we are given an Add this will not
    # work, but the calling code will take care of that.
    shift = S.Zero

    if f.is_Mul:
        args = list(f.args)
    elif isinstance(f, exp):
        args = [f]
    else:
        args = None

    if args:
        newargs = []
        exponentials = []
        while args:
            arg = args.pop()
            if isinstance(arg, exp):
                arg2 = expand(arg)
                if arg2.is_Mul:
                    args += arg2.args
                    continue
                try:
                    a, b = _get_coeff_exp(arg.args[0], x)
                except _CoeffExpValueError:
                    b = 0
                if b == 1:
                    exponentials.append(a)
                else:
                    newargs.append(arg)
            elif arg.is_Pow:
                arg2 = expand(arg)
                if arg2.is_Mul:
                    args += arg2.args
                    continue
                if x not in arg.base.free_symbols:
                    try:
                        a, b = _get_coeff_exp(arg.exp, x)
                    except _CoeffExpValueError:
                        b = 0
                    if b == 1:
                        exponentials.append(a*log(arg.base))
                newargs.append(arg)
            else:
                newargs.append(arg)
        shift = Add(*exponentials)
        f = Mul(*newargs)

    if x not in f.free_symbols:
        _debug('Expression consists of constant and exp shift:', f, shift)
        cond = Eq(im(shift), 0)
        if cond == False:
            _debug('but shift is nonreal, cannot be a Laplace transform')
            return None
        res = f*DiracDelta(t + shift)
        _debug('Result is a delta function, possibly conditional:', res, cond)
        # cond is True or Eq
        return Piecewise((res.subs(t, t_), cond))

    gs = _rewrite1(f, x)
    if gs is not None:
        fac, po, g, cond = gs
        _debug('Could rewrite as single G function:', fac, po, g)
        res = S.Zero
        for C, s, f in g:
            C, f = _rewrite_inversion(fac*C, po*x**s, f, x)
            res += C*_int_inversion(f, x, t)
            cond = And(cond, _check_antecedents_inversion(f, x))
            if cond == False:
                break
        cond = _my_unpolarify(cond)
        if cond == False:
            _debug('But cond is always False.')
        else:
            _debug('Result before branch substitution:', res)
            from sympy.simplify import hyperexpand
            res = _my_unpolarify(hyperexpand(res))
            if not res.has(Heaviside):
                res *= Heaviside(t)
            res = res.subs(t, t + shift)
            if not isinstance(cond, bool):
                cond = cond.subs(t, t + shift)
            from .transforms import InverseLaplaceTransform
            return Piecewise((res.subs(t, t_), cond),
                             (InverseLaplaceTransform(f_.subs(t, t_), x, t_, None), True))

