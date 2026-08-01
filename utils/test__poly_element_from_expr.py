
def test_PolyElement_from_expr():
    x, y, z = symbols("x,y,z")
    R, X, Y, Z = ring((x, y, z), ZZ)

    f = R.from_expr(1)
    assert f == 1 and R.is_element(f)

    f = R.from_expr(x)
    assert f == X and R.is_element(f)

    f = R.from_expr(x*y*z)
    assert f == X*Y*Z and R.is_element(f)

    f = R.from_expr(x*y*z + x*y + x)
    assert f == X*Y*Z + X*Y + X and R.is_element(f)

    f = R.from_expr(x**3*y*z + x**2*y**7 + 1)
    assert f == X**3*Y*Z + X**2*Y**7 + 1 and R.is_element(f)

    r, F = sring([exp(2)])
    f = r.from_expr(exp(2))
    assert f == F[0] and r.is_element(f)

    raises(ValueError, lambda: R.from_expr(1/x))
    raises(ValueError, lambda: R.from_expr(2**x))
    raises(ValueError, lambda: R.from_expr(7*x + sqrt(2)))

    R, = ring("", ZZ)
    f = R.from_expr(1)
    assert f == 1 and R.is_element(f)

