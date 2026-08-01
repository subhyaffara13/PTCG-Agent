
def test_nonlinsolve_abs():
    soln = FiniteSet((y, y), (-y, y))
    assert nonlinsolve([Abs(x) - y], x, y) == soln

