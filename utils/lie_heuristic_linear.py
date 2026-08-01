
def lie_heuristic_linear(match, comp=False):
    r"""
    This heuristic assumes

    1. `\xi = ax + by + c` and
    2. `\eta = fx + gy + h`

    After substituting the following assumptions in the determining PDE, it
    reduces to

    .. math:: f + (g - a)h - bh^{2} - (ax + by + c)\frac{\partial h}{\partial x}
                 - (fx + gy + c)\frac{\partial h}{\partial y}

    Solving the reduced PDE obtained, using the method of characteristics, becomes
    impractical. The method followed is grouping similar terms and solving the system
    of linear equations obtained. The difference between the bivariate heuristic is that
    `h` need not be a rational function in this case.

    References
    ==========
    - E.S. Cheb-Terrab, A.D. Roche, Symmetries and First Order
      ODE Patterns, pp. 10 - pp. 12

    """
    h = match['h']
    hx = match['hx']
    hy = match['hy']
    func = match['func']
    x = func.args[0]
    y = match['y']
    xi = Function('xi')(x, func)
    eta = Function('eta')(x, func)

    coeffdict = {}
    symbols = numbered_symbols("c", cls=Dummy)
    symlist = [next(symbols) for _ in islice(symbols, 6)]
    C0, C1, C2, C3, C4, C5 = symlist
    pde = C3 + (C4 - C0)*h - (C0*x + C1*y + C2)*hx - (C3*x + C4*y + C5)*hy - C1*h**2
    pde, denom = pde.as_numer_denom()
    pde = powsimp(expand(pde))
    if pde.is_Add:
        terms = pde.args
        for term in terms:
            if term.is_Mul:
                rem = Mul(*[m for m in term.args if not m.has(x, y)])
                xypart = term/rem
                if xypart not in coeffdict:
                    coeffdict[xypart] = rem
                else:
                    coeffdict[xypart] += rem
            else:
                if term not in coeffdict:
                    coeffdict[term] = S.One
                else:
                    coeffdict[term] += S.One

    sollist = coeffdict.values()
    soldict = solve(sollist, symlist)
    if soldict:
        if isinstance(soldict, list):
            soldict = soldict[0]
        subval = soldict.values()
        if any(t for t in subval):
            onedict = dict(zip(symlist, [1]*6))
            xival = C0*x + C1*func + C2
            etaval = C3*x + C4*func + C5
            xival = xival.subs(soldict)
            etaval = etaval.subs(soldict)
            xival = xival.subs(onedict)
            etaval = etaval.subs(onedict)
            return [{xi: xival, eta: etaval}]

