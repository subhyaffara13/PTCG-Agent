
def test_diff2():
    n3 = Rational(3)
    n2 = Rational(2)
    n6 = Rational(6)

    e = n3*(-n2 + x**n2)*cos(x) + x*(-n6 + x**n2)*sin(x)
    assert e == 3*(-2 + x**2)*cos(x) + x*(-6 + x**2)*sin(x)
    assert e.diff(x).expand() == x**3*cos(x)

    e = (x + 1)**3
    assert e.diff(x) == 3*(x + 1)**2
    e = x*(x + 1)**3
    assert e.diff(x) == (x + 1)**3 + 3*x*(x + 1)**2
    e = 2*exp(x*x)*x
    assert e.diff(x) == 2*exp(x**2) + 4*x**2*exp(x**2)

