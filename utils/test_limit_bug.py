
def test_limit_bug():
    z = Symbol('z', zero=False)
    assert integrate(sin(x*y*z), (x, 0, pi), (y, 0, pi)).together() == \
        (log(z) - Ci(pi**2*z) + EulerGamma + 2*log(pi))/z

