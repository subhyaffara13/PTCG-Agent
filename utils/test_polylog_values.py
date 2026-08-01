
def test_polylog_values():
    assert polylog(2, 2) == pi**2/4 - I*pi*log(2)
    assert polylog(2, S.Half) == pi**2/12 - log(2)**2/2
    for z in [S.Half, 2, (sqrt(5)-1)/2, -(sqrt(5)-1)/2, -(sqrt(5)+1)/2, (3-sqrt(5))/2]:
        assert Abs(polylog(2, z).evalf() - polylog(2, z, evaluate=False).evalf()) < 1e-15
    z = Symbol("z")
    for s in [-1, 0]:
        for _ in range(10):
            assert verify_numerically(polylog(s, z), polylog(s, z, evaluate=False),
                                      z, a=-3, b=-2, c=S.Half, d=2)
            assert verify_numerically(polylog(s, z), polylog(s, z, evaluate=False),
                                      z, a=2, b=-2, c=5, d=2)

    from sympy.integrals.integrals import Integral
    assert polylog(0, Integral(1, (x, 0, 1))) == -S.Half

