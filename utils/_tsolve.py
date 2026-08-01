
def _tsolve(eq, sym, **flags):
    """
    Helper for ``_solve`` that solves a transcendental equation with respect
    to the given symbol. Various equations containing powers and logarithms,
    can be solved.

    There is currently no guarantee that all solutions will be returned or
    that a real solution will be favored over a complex one.

    Either a list of potential solutions will be returned or None will be
    returned (in the case that no method was known to get a solution
    for the equation). All other errors (like the inability to cast an
    expression as a Poly) are unhandled.

    Examples
    ========

    >>> from sympy import log, ordered
    >>> from sympy.solvers.solvers import _tsolve as tsolve
    >>> from sympy.abc import x

    >>> list(ordered(tsolve(3**(2*x + 5) - 4, x)))
    [-5/2 + log(2)/log(3), (-5*log(3)/2 + log(2) + I*pi)/log(3)]

    >>> tsolve(log(x) + 2*x, x)
    [LambertW(2)/2]

    """
    if 'tsolve_saw' not in flags:
        flags['tsolve_saw'] = []
    if eq in flags['tsolve_saw']:
        return None
    else:
        flags['tsolve_saw'].append(eq)

    rhs, lhs = _invert(eq, sym)

    if lhs == sym:
        return [rhs]
    try:
        if lhs.is_Add:
            # it's time to try factoring; powdenest is used
            # to try get powers in standard form for better factoring
            f = factor(powdenest(lhs - rhs))
            if f.is_Mul:
                return _vsolve(f, sym, **flags)
            if rhs:
                f = logcombine(lhs, force=flags.get('force', True))
                if f.count(log) != lhs.count(log):
                    if isinstance(f, log):
                        return _vsolve(f.args[0] - exp(rhs), sym, **flags)
                    return _tsolve(f - rhs, sym, **flags)

        elif lhs.is_Pow:
            if lhs.exp.is_Integer:
                if lhs - rhs != eq:
                    return _vsolve(lhs - rhs, sym, **flags)

            if sym not in lhs.exp.free_symbols:
                return _vsolve(lhs.base - rhs**(1/lhs.exp), sym, **flags)

            # _tsolve calls this with Dummy before passing the actual number in.
            if any(t.is_Dummy for t in rhs.free_symbols):
                raise NotImplementedError # _tsolve will call here again...

            # a ** g(x) == 0
            if not rhs:
                # f(x)**g(x) only has solutions where f(x) == 0 and g(x) != 0 at
                # the same place
                sol_base = _vsolve(lhs.base, sym, **flags)
                return [s for s in sol_base if lhs.exp.subs(sym, s) != 0]  # XXX use checksol here?

            # a ** g(x) == b
            if not lhs.base.has(sym):
                if lhs.base == 0:
                    return _vsolve(lhs.exp, sym, **flags) if rhs != 0 else []

                # Gets most solutions...
                if lhs.base == rhs.as_base_exp()[0]:
                    # handles case when bases are equal
                    sol = _vsolve(lhs.exp - rhs.as_base_exp()[1], sym, **flags)
                else:
                    # handles cases when bases are not equal and exp
                    # may or may not be equal
                    f = exp(log(lhs.base)*lhs.exp) - exp(log(rhs))
                    sol = _vsolve(f, sym, **flags)

                # Check for duplicate solutions
                def equal(expr1, expr2):
                    _ = Dummy()
                    eq = checksol(expr1 - _, _, expr2)
                    if eq is None:
                        if nsimplify(expr1) != nsimplify(expr2):
                            return False
                        # they might be coincidentally the same
                        # so check more rigorously
                        eq = expr1.equals(expr2)  # XXX expensive but necessary?
                    return eq

                # Guess a rational exponent
                e_rat = nsimplify(log(abs(rhs))/log(abs(lhs.base)))
                e_rat = simplify(posify(e_rat)[0])
                n, d = fraction(e_rat)
                if expand(lhs.base**n - rhs**d) == 0:
                    sol = [s for s in sol if not equal(lhs.exp.subs(sym, s), e_rat)]
                    sol.extend(_vsolve(lhs.exp - e_rat, sym, **flags))

                return list(set(sol))

            # f(x) ** g(x) == c
            else:
                sol = []
                logform = lhs.exp*log(lhs.base) - log(rhs)
                if logform != lhs - rhs:
                    try:
                        sol.extend(_vsolve(logform, sym, **flags))
                    except NotImplementedError:
                        pass

                # Collect possible solutions and check with substitution later.
                check = []
                if rhs == 1:
                    # f(x) ** g(x) = 1 -- g(x)=0 or f(x)=+-1
                    check.extend(_vsolve(lhs.exp, sym, **flags))
                    check.extend(_vsolve(lhs.base - 1, sym, **flags))
                    check.extend(_vsolve(lhs.base + 1, sym, **flags))
                elif rhs.is_Rational:
                    for d in (i for i in divisors(abs(rhs.p)) if i != 1):
                        e, t = integer_log(rhs.p, d)
                        if not t:
                            continue  # rhs.p != d**b
                        for s in divisors(abs(rhs.q)):
                            if s**e== rhs.q:
                                r = Rational(d, s)
                                check.extend(_vsolve(lhs.base - r, sym, **flags))
                                check.extend(_vsolve(lhs.base + r, sym, **flags))
                                check.extend(_vsolve(lhs.exp - e, sym, **flags))
                elif rhs.is_irrational:
                    b_l, e_l = lhs.base.as_base_exp()
                    n, d = (e_l*lhs.exp).as_numer_denom()
                    b, e = sqrtdenest(rhs).as_base_exp()
                    check = [sqrtdenest(i) for i in (_vsolve(lhs.base - b, sym, **flags))]
                    check.extend([sqrtdenest(i) for i in (_vsolve(lhs.exp - e, sym, **flags))])
                    if e_l*d != 1:
                        check.extend(_vsolve(b_l**n - rhs**(e_l*d), sym, **flags))
                for s in check:
                    ok = checksol(eq, sym, s)
                    if ok is None:
                        ok = eq.subs(sym, s).equals(0)
                    if ok:
                        sol.append(s)
                return list(set(sol))

        elif lhs.is_Function and len(lhs.args) == 1:
            if lhs.func in multi_inverses:
                # sin(x) = 1/3 -> x - asin(1/3) & x - (pi - asin(1/3))
                soln = []
                for i in multi_inverses[type(lhs)](rhs):
                    soln.extend(_vsolve(lhs.args[0] - i, sym, **flags))
                return list(set(soln))
            elif lhs.func == LambertW:
                return _vsolve(lhs.args[0] - rhs*exp(rhs), sym, **flags)

        rewrite = lhs.rewrite(exp)
        rewrite = rebuild(rewrite) # avoid rewrites involving evaluate=False
        if rewrite != lhs:
            return _vsolve(rewrite - rhs, sym, **flags)
    except NotImplementedError:
        pass

    # maybe it is a lambert pattern
    if flags.pop('bivariate', True):
        # lambert forms may need some help being recognized, e.g. changing
        # 2**(3*x) + x**3*log(2)**3 + 3*x**2*log(2)**2 + 3*x*log(2) + 1
        # to 2**(3*x) + (x*log(2) + 1)**3

        # make generator in log have exponent of 1
        logs = eq.atoms(log)
        spow = min(
            {i.exp for j in logs for i in j.atoms(Pow)
             if i.base == sym} or {1})
        if spow != 1:
            p = sym**spow
            u = Dummy('bivariate-cov')
            ueq = eq.subs(p, u)
            if not ueq.has_free(sym):
                sol = _vsolve(ueq, u, **flags)
                inv = _vsolve(p - u, sym)
                return [i.subs(u, s) for i in inv for s in sol]

        g = _filtered_gens(eq.as_poly(), sym)
        up_or_log = set()
        for gi in g:
            if isinstance(gi, (exp, log)) or (gi.is_Pow and gi.base == S.Exp1):
                up_or_log.add(gi)
            elif gi.is_Pow:
                gisimp = powdenest(expand_power_exp(gi))
                if gisimp.is_Pow and sym in gisimp.exp.free_symbols:
                    up_or_log.add(gi)
        eq_down = expand_log(expand_power_exp(eq)).subs(
            dict(list(zip(up_or_log, [0]*len(up_or_log)))))
        eq = expand_power_exp(factor(eq_down, deep=True) + (eq - eq_down))
        rhs, lhs = _invert(eq, sym)
        if lhs.has(sym):
            try:
                poly = lhs.as_poly()
                g = _filtered_gens(poly, sym)
                _eq = lhs - rhs
                sols = _solve_lambert(_eq, sym, g)
                # use a simplified form if it satisfies eq
                # and has fewer operations
                for n, s in enumerate(sols):
                    ns = nsimplify(s)
                    if ns != s and ns.count_ops() <= s.count_ops():
                        ok = checksol(_eq, sym, ns)
                        if ok is None:
                            ok = _eq.subs(sym, ns).equals(0)
                        if ok:
                            sols[n] = ns
                return sols
            except NotImplementedError:
                # maybe it's a convoluted function
                if len(g) == 2:
                    try:
                        gpu = bivariate_type(lhs - rhs, *g)
                        if gpu is None:
                            raise NotImplementedError
                        g, p, u = gpu
                        flags['bivariate'] = False
                        inversion = _tsolve(g - u, sym, **flags)
                        if inversion:
                            sol = _vsolve(p, u, **flags)
                            return list({i.subs(u, s)
                                for i in inversion for s in sol})
                    except NotImplementedError:
                        pass
                else:
                    pass

    if flags.pop('force', True):
        flags['force'] = False
        pos, reps = posify(lhs - rhs)
        if rhs == S.ComplexInfinity:
            return []
        for u, s in reps.items():
            if s == sym:
                break
        else:
            u = sym
        if pos.has(u):
            try:
                soln = _vsolve(pos, u, **flags)
                return [s.subs(reps) for s in soln]
            except NotImplementedError:
                pass
        else:
            pass  # here for coverage

    return  # here for coverage

