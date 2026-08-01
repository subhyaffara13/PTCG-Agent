
def _coefficient_t(p, t):
    r"""Coefficient of `x_i**j` in p, where ``t`` = (i, j)"""
    i, j = t
    R = p.ring
    expv1 = [0]*R.ngens
    expv1[i] = j
    expv1 = tuple(expv1)
    p1 = R(0)
    for expv in p:
        if expv[i] == j:
            p1[monomial_div(expv, expv1)] = p[expv]
    return p1

