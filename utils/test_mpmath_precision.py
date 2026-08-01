
def test_mpmath_precision():
    mpmath.mp.dps = 100
    assert str(lambdify((), pi.evalf(100), 'mpmath')()) == str(pi.evalf(100))

