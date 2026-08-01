
def _check_varsh_sum_871_1(e):
    a = Wild('a')
    alpha = symbols('alpha')
    b = Wild('b')
    match = e.match(Sum(CG(a, alpha, b, 0, a, alpha), (alpha, -a, a)))
    if match is not None and len(match) == 2:
        return ((2*a + 1)*KroneckerDelta(b, 0)).subs(match)
    return e

