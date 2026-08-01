
def test_V7():
    r1 = integrate(sinh(x)**4/cosh(x)**2)
    assert r1.simplify() == x*R(-3, 2) + sinh(x)**3/(2*cosh(x)) + 3*tanh(x)/2

