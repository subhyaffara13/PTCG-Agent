
def _check_varsh_sum_871_2(e):
    a = Wild('a')
    alpha = symbols('alpha')
    c = Wild('c')
    match = e.match(
        Sum((-1)**(a - alpha)*CG(a, alpha, a, -alpha, c, 0), (alpha, -a, a)))
    if match is not None and len(match) == 2:
        return (sqrt(2*a + 1)*KroneckerDelta(c, 0)).subs(match)
    return e

