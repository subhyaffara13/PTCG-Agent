
def _eqs2dict(eqs, funcs):
    eqsorig = {}
    eqsmap = {}
    funcset = set(funcs)
    for eq in eqs:
        f1, = eq.lhs.atoms(AppliedUndef)
        f2s = (eq.rhs.atoms(AppliedUndef) - {f1}) & funcset
        eqsmap[f1] = f2s
        eqsorig[f1] = eq
    return eqsmap, eqsorig

