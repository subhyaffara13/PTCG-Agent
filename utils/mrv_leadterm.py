
def mrv_leadterm(e, x):
    """Returns (c0, e0) for e."""
    Omega = SubsSet()
    if not e.has(x):
        return (e, S.Zero)
    if Omega == SubsSet():
        Omega, exps = mrv(e, x)
    if not Omega:
        # e really does not depend on x after simplification
        return exps, S.Zero
    if x in Omega:
        # move the whole omega up (exponentiate each term):
        Omega_up = moveup2(Omega, x)
        exps_up = moveup([exps], x)[0]
        # NOTE: there is no need to move this down!
        Omega = Omega_up
        exps = exps_up
    #
    # The positive dummy, w, is used here so log(w*2) etc. will expand;
    # a unique dummy is needed in this algorithm
    #
    # For limits of complex functions, the algorithm would have to be
    # improved, or just find limits of Re and Im components separately.
    #
    w = Dummy("w", positive=True)
    f, logw = rewrite(exps, Omega, x, w)

    # Ensure expressions of the form exp(log(...)) don't get simplified automatically in the previous steps.
    # see: https://github.com/sympy/sympy/issues/15323#issuecomment-478639399
    f = f.replace(lambda f: f.is_Pow and f.has(x), lambda f: exp(log(f.base)*f.exp))

    try:
        lt = f.leadterm(w, logx=logw)
    except (NotImplementedError, PoleError, ValueError):
        n0 = 1
        _series = Order(1)
        incr = S.One
        while _series.is_Order:
            _series = f._eval_nseries(w, n=n0+incr, logx=logw)
            incr *= 2
        series = _series.expand().removeO()
        try:
            lt = series.leadterm(w, logx=logw)
        except (NotImplementedError, PoleError, ValueError):
            lt = f.as_coeff_exponent(w)
            if lt[0].has(w):
                base = f.as_base_exp()[0].as_coeff_exponent(w)
                ex = f.as_base_exp()[1]
                lt = (base[0]**ex, base[1]*ex)
    return (lt[0].subs(log(w), logw), lt[1])

