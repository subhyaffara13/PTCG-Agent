
def test_linsolve_large_sparse():
    #
    # This is mainly a performance test
    #

    def _mk_eqs_sol(n):
        xs = symbols('x:{}'.format(n))
        ys = symbols('y:{}'.format(n))
        syms = xs + ys
        eqs = []
        sol = (-S.Half,) * n + (S.Half,) * n
        for xi, yi in zip(xs, ys):
            eqs.extend([xi + yi, xi - yi + 1])
        return eqs, syms, FiniteSet(sol)

    n = 500
    eqs, syms, sol = _mk_eqs_sol(n)
    assert linsolve(eqs, syms) == sol

