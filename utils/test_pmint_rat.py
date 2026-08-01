
def test_pmint_rat():
    # TODO: heurisch() is off by a constant: -3/4. Possibly different permutation
    # would give the optimal result?

    def drop_const(expr, x):
        if expr.is_Add:
            return Add(*[ arg for arg in expr.args if arg.has(x) ])
        else:
            return expr

    f = (x**7 - 24*x**4 - 4*x**2 + 8*x - 8)/(x**8 + 6*x**6 + 12*x**4 + 8*x**2)
    g = (4 + 8*x**2 + 6*x + 3*x**3)/(x**5 + 4*x**3 + 4*x) + log(x)

    assert drop_const(ratsimp(heurisch(f, x)), x) == g

