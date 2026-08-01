
def test_FracElement_from_expr():
    x, y, z = symbols("x,y,z")
    F, X, Y, Z = field((x, y, z), ZZ)

    f = F.from_expr(1)
    assert f == 1 and F.is_element(f)

    f = F.from_expr(Rational(3, 7))
    assert f == F(3)/7 and F.is_element(f)

    f = F.from_expr(x)
    assert f == X and F.is_element(f)

    f = F.from_expr(Rational(3,7)*x)
    assert f == X*Rational(3, 7) and F.is_element(f)

    f = F.from_expr(1/x)
    assert f == 1/X and F.is_element(f)

    f = F.from_expr(x*y*z)
    assert f == X*Y*Z and F.is_element(f)

    f = F.from_expr(x*y/z)
    assert f == X*Y/Z and F.is_element(f)

    f = F.from_expr(x*y*z + x*y + x)
    assert f == X*Y*Z + X*Y + X and F.is_element(f)

    f = F.from_expr((x*y*z + x*y + x)/(x*y + 7))
    assert f == (X*Y*Z + X*Y + X)/(X*Y + 7) and F.is_element(f)

    f = F.from_expr(x**3*y*z + x**2*y**7 + 1)
    assert f == X**3*Y*Z + X**2*Y**7 + 1 and F.is_element(f)

    raises(ValueError, lambda: F.from_expr(2**x))
    raises(ValueError, lambda: F.from_expr(7*x + sqrt(2)))

    assert isinstance(ZZ[2**x].get_field().convert(2**(-x)),
        FracElement)
    assert isinstance(ZZ[x**2].get_field().convert(x**(-6)),
        FracElement)
    assert isinstance(ZZ[exp(Rational(1, 3))].get_field().convert(E),
        FracElement)

