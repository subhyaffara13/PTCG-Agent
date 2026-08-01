
def _check_varsh_sum_872_4(e):
    alpha = symbols('alpha')
    beta = symbols('beta')
    a = Wild('a')
    b = Wild('b')
    c = Wild('c')
    cp = Wild('cp')
    gamma = Wild('gamma')
    gammap = Wild('gammap')
    cg1 = CG(a, alpha, b, beta, c, gamma)
    cg2 = CG(a, alpha, b, beta, cp, gammap)
    match1 = e.match(Sum(cg1*cg2, (alpha, -a, a), (beta, -b, b)))
    if match1 is not None and len(match1) == 6:
        return (KroneckerDelta(c, cp)*KroneckerDelta(gamma, gammap)).subs(match1)
    match2 = e.match(Sum(cg1**2, (alpha, -a, a), (beta, -b, b)))
    if match2 is not None and len(match2) == 4:
        return S.One
    return e

