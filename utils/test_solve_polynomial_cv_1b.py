
def test_solve_polynomial_cv_1b():
    assert set(solve(4*x*(1 - a*sqrt(x)), x)) == {S.Zero, 1/a**2}
    assert set(solve(x*(root(x, 3) - 3), x)) == {S.Zero, S(27)}

