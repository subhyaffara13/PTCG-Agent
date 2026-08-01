
def test_sympy_lambda():
    mpmath.mp.dps = 50
    sin02 = mpmath.mpf("0.19866933079506121545941262711838975037020672954020")
    f = lambdify(x, sin(x), "sympy")
    assert f(x) == sin(x)
    prec = 1e-15
    assert -prec < f(Rational(1, 5)).evalf() - Float(str(sin02)) < prec

