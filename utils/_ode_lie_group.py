
def _ode_lie_group( s, func, order, match):

    heuristics = lie_heuristics
    inf = {}
    f = func.func
    x = func.args[0]
    df = func.diff(x)
    xi = Function("xi")
    eta = Function("eta")
    xis = match['xi']
    etas = match['eta']
    y = match.pop('y', None)
    if y:
        h = -simplify(match[match['d']]/match[match['e']])
    else:
        y = Dummy("y")
        h = s.subs(func, y)

    if xis is not None and etas is not None:
        inf = [{xi(x, f(x)): S(xis), eta(x, f(x)): S(etas)}]

        if checkinfsol(Eq(df, s), inf, func=f(x), order=1)[0][0]:
            heuristics = ["user_defined"] + list(heuristics)

    match = {'h': h, 'y': y}

    # This is done so that if any heuristic raises a ValueError
    # another heuristic can be used.
    sol = None
    for heuristic in heuristics:
        sol = _ode_lie_group_try_heuristic(Eq(df, s), heuristic, func, match, inf)
        if sol:
            return sol
    return sol

