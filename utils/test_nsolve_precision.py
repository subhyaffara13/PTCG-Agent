
def test_nsolve_precision():
    x, y = symbols('x y')
    sol = nsolve(x**2 - pi, x, 3, prec=128)
    assert abs(sqrt(pi).evalf(128) - sol) < 1e-128
    assert isinstance(sol, Float)

    sols = nsolve((y**2 - x, x**2 - pi), (x, y), (3, 3), prec=128)
    assert isinstance(sols, Matrix)
    assert sols.shape == (2, 1)
    assert abs(sqrt(pi).evalf(128) - sols[0]) < 1e-128
    assert abs(sqrt(sqrt(pi)).evalf(128) - sols[1]) < 1e-128
    assert all(isinstance(i, Float) for i in sols)

