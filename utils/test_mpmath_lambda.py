
def test_mpmath_lambda():
    mpmath.mp.dps = 50
    sin02 = mpmath.mpf("0.19866933079506121545941262711838975037020672954020")
    f = lambdify(x, sin(x), "mpmath")
    prec = 1e-49  # mpmath precision is around 50 decimal places
    assert -prec < f(mpmath.mpf("0.2")) - sin02 < prec
    raises(TypeError, lambda: f(x))
           # if this succeeds, it can't be a mpmath function

    ref2 = (mpmath.mpf("1e-30")
            - mpmath.mpf("1e-45")/2
            + 5*mpmath.mpf("1e-60")/6
            - 3*mpmath.mpf("1e-75")/4
            + 33*mpmath.mpf("1e-90")/40
            )
    f2a = lambdify((x, y), x**y - 1, "mpmath")
    f2b = lambdify((x, y), powm1(x, y), "mpmath")
    f2c = lambdify((x,), expm1(x*log1p(x)), "mpmath")
    ans2a = f2a(mpmath.mpf("1")+mpmath.mpf("1e-15"), mpmath.mpf("1e-15"))
    ans2b = f2b(mpmath.mpf("1")+mpmath.mpf("1e-15"), mpmath.mpf("1e-15"))
    ans2c = f2c(mpmath.mpf("1e-15"))
    assert abs(ans2a - ref2) < 1e-51
    assert abs(ans2b - ref2) < 1e-67
    assert abs(ans2c - ref2) < 1e-80

