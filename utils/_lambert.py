
def _lambert(eq, x):
    """
    Given an expression assumed to be in the form
        ``F(X, a..f) = a*log(b*X + c) + d*X + f = 0``
    where X = g(x) and x = g^-1(X), return the Lambert solution,
        ``x = g^-1(-c/b + (a/d)*W(d/(a*b)*exp(c*d/a/b)*exp(-f/a)))``.
    """
    eq = _mexpand(expand_log(eq))
    mainlog = _mostfunc(eq, log, x)
    if not mainlog:
        return []  # violated assumptions
    other = eq.subs(mainlog, 0)
    if isinstance(-other, log):
        eq = (eq - other).subs(mainlog, mainlog.args[0])
        mainlog = mainlog.args[0]
        if not isinstance(mainlog, log):
            return []  # violated assumptions
        other = -(-other).args[0]
        eq += other
    if x not in other.free_symbols:
        return [] # violated assumptions
    d, f, X2 = _linab(other, x)
    logterm = collect(eq - other, mainlog)
    a = logterm.as_coefficient(mainlog)
    if a is None or x in a.free_symbols:
        return []  # violated assumptions
    logarg = mainlog.args[0]
    b, c, X1 = _linab(logarg, x)
    if X1 != X2:
        return []  # violated assumptions

    # invert the generator X1 so we have x(u)
    u = Dummy('rhs')
    xusolns = solve(X1 - u, x)

    # There are infinitely many branches for LambertW
    # but only branches for k = -1 and 0 might be real. The k = 0
    # branch is real and the k = -1 branch is real if the LambertW argument
    # in in range [-1/e, 0]. Since `solve` does not return infinite
    # solutions we will only include the -1 branch if it tests as real.
    # Otherwise, inclusion of any LambertW in the solution indicates to
    #  the user that there are imaginary solutions corresponding to
    # different k values.
    lambert_real_branches = [-1, 0]
    sol = []

    # solution of the given Lambert equation is like
    # sol = -c/b + (a/d)*LambertW(arg, k),
    # where arg = d/(a*b)*exp((c*d-b*f)/a/b) and k in lambert_real_branches.
    # Instead of considering the single arg, `d/(a*b)*exp((c*d-b*f)/a/b)`,
    # the individual `p` roots obtained when writing `exp((c*d-b*f)/a/b)`
    # as `exp(A/p) = exp(A)**(1/p)`, where `p` is an Integer, are used.

    # calculating args for LambertW
    num, den = ((c*d-b*f)/a/b).as_numer_denom()
    p, den = den.as_coeff_Mul()
    e = exp(num/den)
    t = Dummy('t')
    args = [d/(a*b)*t for t in roots(t**p - e, t).keys()]

    # calculating solutions from args
    for arg in args:
        for k in lambert_real_branches:
            w = LambertW(arg, k)
            if k and not w.is_real:
                continue
            rhs = -c/b + (a/d)*w

            sol.extend(xu.subs(u, rhs) for xu in xusolns)
    return sol

