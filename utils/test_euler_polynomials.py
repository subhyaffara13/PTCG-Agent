
def test_euler_polynomials():
    assert euler(0, x) == 1
    assert euler(1, x) == x - S.Half
    assert euler(2, x) == x**2 - x
    assert euler(3, x) == x**3 - (3*x**2)/2 + Rational(1, 4)
    m = Symbol('m')
    assert isinstance(euler(m, x), euler)
    from sympy.core.numbers import Float
    A = Float('-0.46237208575048694923364757452876131e8')  # from Maple
    B = euler(19, S.Pi).evalf(32)
    assert abs((A - B)/A) < 1e-31
    z = Float(0.1) + Float(0.2)*I
    expected = Float(-3126.54721663773 ) + Float(565.736261497056) * I
    assert abs(euler(13, z) - expected) < 1e-10

