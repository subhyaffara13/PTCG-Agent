
def _helper_simplify(eq, hint, func, order, match, solvefun):
    """Helper function of pdsolve that calls the respective
    pde functions to solve for the partial differential
    equations. This minimizes the computation in
    calling _desolve multiple times.
    """
    solvefunc = globals()["pde_" + hint.removesuffix("_Integral")]
    return _handle_Integral(solvefunc(eq, func, order,
        match, solvefun), func, order, hint)


def _helper_simplify(eq, hint, match, simplify=True, ics=None, **kwargs):
    r"""
    Helper function of dsolve that calls the respective
    :py:mod:`~sympy.solvers.ode` functions to solve for the ordinary
    differential equations. This minimizes the computation in calling
    :py:meth:`~sympy.solvers.deutils._desolve` multiple times.
    """
    r = match
    func = r['func']
    order = r['order']
    match = r[hint]

    if isinstance(match, SingleODESolver):
        solvefunc = match
    else:
        solvefunc = globals()['ode_' + hint.removesuffix('_Integral')]

    free = eq.free_symbols
    cons = lambda s: s.free_symbols.difference(free)

    if simplify:
        # odesimp() will attempt to integrate, if necessary, apply constantsimp(),
        # attempt to solve for func, and apply any other hint specific
        # simplifications
        if isinstance(solvefunc, SingleODESolver):
            sols = solvefunc.get_general_solution()
        else:
            sols = solvefunc(eq, func, order, match)
        if iterable(sols):
            rv = []
            for s in sols:
                simp = odesimp(eq, s, func, hint)
                if iterable(simp):
                    rv.extend(simp)
                else:
                    rv.append(simp)
        else:
            rv = odesimp(eq, sols, func, hint)
    else:
        # We still want to integrate (you can disable it separately with the hint)
        if isinstance(solvefunc, SingleODESolver):
            exprs = solvefunc.get_general_solution(simplify=False)
        else:
            match['simplify'] = False  # Some hints can take advantage of this option
            exprs = solvefunc(eq, func, order, match)
        if isinstance(exprs, list):
            rv = [_handle_Integral(expr, func, hint) for expr in exprs]
        else:
            rv = _handle_Integral(exprs, func, hint)

    if isinstance(rv, list):
        assert all(isinstance(i, Eq) for i in rv), rv  # if not => internal error
        if simplify:
            rv = _remove_redundant_solutions(eq, rv, order, func.args[0])
        if len(rv) == 1:
            rv = rv[0]
    if ics and 'power_series' not in hint:
        if isinstance(rv, (Expr, Eq)):
            solved_constants = solve_ics([rv], [r['func']], cons(rv), ics)
            rv = rv.subs(solved_constants)
        else:
            rv1 = []
            for s in rv:
                try:
                    solved_constants = solve_ics([s], [r['func']], cons(s), ics)
                except ValueError:
                    continue
                rv1.append(s.subs(solved_constants))
            if len(rv1) == 1:
                return rv1[0]
            rv = rv1
    return rv

