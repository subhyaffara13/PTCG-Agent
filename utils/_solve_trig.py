
def _solve_trig(f, symbol, domain):
    """Function to call other helpers to solve trigonometric equations """
    # If f is composed of a single trig function (potentially appearing multiple
    # times) we should solve by either inverting directly or inverting after a
    # suitable change of variable.
    #
    # _solve_trig is currently only called by _solveset for trig/hyperbolic
    # functions of an argument linear in x. Inverting a symbolic argument should
    # include a guard against division by zero in order to have a result that is
    # consistent with similar processing done by _solve_trig1.
    # (Ideally _invert should add these conditions by itself.)
    trig_expr, count = None, 0
    for expr in preorder_traversal(f):
        if isinstance(expr, (TrigonometricFunction,
                            HyperbolicFunction)) and expr.has(symbol):
            if not trig_expr:
                trig_expr, count = expr, 1
            elif expr == trig_expr:
                count += 1
            else:
                trig_expr, count = False, 0
                break
    if count == 1:
        # direct inversion
        x, sol = _invert(f, 0, symbol, domain)
        if x == symbol:
            cond = True
            if trig_expr.free_symbols - {symbol}:
                a, h = trig_expr.args[0].as_independent(symbol, as_Add=True)
                m, h = h.as_independent(symbol, as_Add=False)
                num, den = m.as_numer_denom()
                cond = Ne(num, 0) & Ne(den, 0)
            return ConditionSet(symbol, cond, sol)
        else:
            return ConditionSet(symbol, Eq(f, 0), domain)
    elif count:
        # solve by change of variable
        y = Dummy('y')
        f_cov = f.subs(trig_expr, y)
        sol_cov = solveset(f_cov, y, domain)
        if isinstance(sol_cov, FiniteSet):
            return Union(
                *[_solve_trig(trig_expr-s, symbol, domain) for s in sol_cov])

    sol = None
    try:
        # multiple trig/hyp functions; solve by rewriting to exp
        sol = _solve_trig1(f, symbol, domain)
    except _SolveTrig1Error:
        try:
            # multiple trig/hyp functions; solve by rewriting to tan(x/2)
            sol = _solve_trig2(f, symbol, domain)
        except ValueError:
            raise NotImplementedError(filldedent('''
                Solution to this kind of trigonometric equations
                is yet to be implemented'''))
    return sol

