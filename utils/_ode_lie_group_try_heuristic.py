
def _ode_lie_group_try_heuristic(eq, heuristic, func, match, inf):

    xi = Function("xi")
    eta = Function("eta")
    f = func.func
    x = func.args[0]
    y = match['y']
    h = match['h']
    tempsol = []
    if not inf:
        try:
            inf = infinitesimals(eq, hint=heuristic, func=func, order=1, match=match)
        except ValueError:
            return None
    for infsim in inf:
        xiinf = (infsim[xi(x, func)]).subs(func, y)
        etainf = (infsim[eta(x, func)]).subs(func, y)
        # This condition creates recursion while using pdsolve.
        # Since the first step while solving a PDE of form
        # a*(f(x, y).diff(x)) + b*(f(x, y).diff(y)) + c = 0
        # is to solve the ODE dy/dx = b/a
        if simplify(etainf/xiinf) == h:
            continue
        rpde = f(x, y).diff(x)*xiinf + f(x, y).diff(y)*etainf
        r = pdsolve(rpde, func=f(x, y)).rhs
        s = pdsolve(rpde - 1, func=f(x, y)).rhs
        newcoord = [_lie_group_remove(coord) for coord in [r, s]]
        r = Dummy("r")
        s = Dummy("s")
        C1 = Symbol("C1")
        rcoord = newcoord[0]
        scoord = newcoord[-1]
        try:
            sol = solve([r - rcoord, s - scoord], x, y, dict=True)
            if sol == []:
                continue
        except NotImplementedError:
            continue
        else:
            sol = sol[0]
            xsub = sol[x]
            ysub = sol[y]
            num = simplify(scoord.diff(x) + scoord.diff(y)*h)
            denom = simplify(rcoord.diff(x) + rcoord.diff(y)*h)
            if num and denom:
                diffeq = simplify((num/denom).subs([(x, xsub), (y, ysub)]))
                sep = separatevars(diffeq, symbols=[r, s], dict=True)
                if sep:
                    # Trying to separate, r and s coordinates
                    deq = integrate((1/sep[s]), s) + C1 - integrate(sep['coeff']*sep[r], r)
                    # Substituting and reverting back to original coordinates
                    deq = deq.subs([(r, rcoord), (s, scoord)])
                    try:
                        sdeq = solve(deq, y)
                    except NotImplementedError:
                        tempsol.append(deq)
                    else:
                        return [Eq(f(x), sol) for sol in sdeq]


            elif denom: # (ds/dr) is zero which means s is constant
                return [Eq(f(x), solve(scoord - C1, y)[0])]

            elif num: # (dr/ds) is zero which means r is constant
                return [Eq(f(x), solve(rcoord - C1, y)[0])]

    # If nothing works, return solution as it is, without solving for y
    if tempsol:
        return [Eq(sol.subs(y, f(x)), 0) for sol in tempsol]
    return None

