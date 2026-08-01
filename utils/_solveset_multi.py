
def _solveset_multi(eqs, syms, domains):
    '''Basic implementation of a multivariate solveset.

    For internal use (not ready for public consumption)'''

    rep = {}
    for sym, dom in zip(syms, domains):
        if dom is S.Reals:
            rep[sym] = Symbol(sym.name, real=True)
    eqs = [eq.subs(rep) for eq in eqs]
    syms = [sym.subs(rep) for sym in syms]

    syms = tuple(syms)

    if len(eqs) == 0:
        return ProductSet(*domains)

    if len(syms) == 1:
        sym = syms[0]
        domain = domains[0]
        solsets = [solveset(eq, sym, domain) for eq in eqs]
        solset = Intersection(*solsets)
        return ImageSet(Lambda((sym,), (sym,)), solset).doit()

    eqs = sorted(eqs, key=lambda eq: len(eq.free_symbols & set(syms)))

    for n, eq in enumerate(eqs):
        sols = []
        all_handled = True
        for sym in syms:
            if sym not in eq.free_symbols:
                continue
            sol = solveset(eq, sym, domains[syms.index(sym)])

            if isinstance(sol, FiniteSet):
                i = syms.index(sym)
                symsp = syms[:i] + syms[i+1:]
                domainsp = domains[:i] + domains[i+1:]
                eqsp = eqs[:n] + eqs[n+1:]
                for s in sol:
                    eqsp_sub = [eq.subs(sym, s) for eq in eqsp]
                    sol_others = _solveset_multi(eqsp_sub, symsp, domainsp)
                    fun = Lambda((symsp,), symsp[:i] + (s,) + symsp[i:])
                    sols.append(ImageSet(fun, sol_others).doit())
            else:
                all_handled = False
        if all_handled:
            return Union(*sols)

