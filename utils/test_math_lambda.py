
def test_math_lambda():
    mpmath.mp.dps = 50
    sin02 = mpmath.mpf("0.19866933079506121545941262711838975037020672954020")
    f = lambdify(x, sin(x), "math")
    prec = 1e-15
    assert -prec < f(0.2) - sin02 < prec
    raises(TypeError, lambda: f(x))

