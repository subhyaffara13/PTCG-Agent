
def test_lambdify__arguments_with_invalid_python_identifiers():
    # see sympy/sympy#26690
    N = CoordSys3D('N')
    xn, yn, zn = N.base_scalars()
    expr = xn + yn
    f = lambdify([xn, yn], expr)
    res = f(0.2, 0.3)
    ref = 0.2 + 0.3
    assert abs(res-ref) < 1e-15

