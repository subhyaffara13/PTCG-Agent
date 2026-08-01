
def test_W12():
    p = symbols('p', positive=True)
    q = symbols('q', real=True)
    r1 = integrate(x*exp(-p*x**2 + 2*q*x), (x, -oo, oo))
    assert r1.simplify() == sqrt(pi)*q*exp(q**2/p)/p**R(3, 2)

