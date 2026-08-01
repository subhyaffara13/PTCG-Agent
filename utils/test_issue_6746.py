
def test_issue_6746():
    y = Symbol('y')
    n = Symbol('n')
    assert manualintegrate(y**x, x) == Piecewise(
        (y**x/log(y), Ne(log(y), 0)), (x, True))
    assert manualintegrate(y**(n*x), x) == Piecewise(
        (Piecewise(
            (y**(n*x)/log(y), Ne(log(y), 0)),
            (n*x, True)
        )/n, Ne(n, 0)),
        (x, True))
    assert manualintegrate(exp(n*x), x) == Piecewise(
        (exp(n*x)/n, Ne(n, 0)), (x, True))

    y = Symbol('y', positive=True)
    assert manualintegrate((y + 1)**x, x) == (y + 1)**x/log(y + 1)
    y = Symbol('y', zero=True)
    assert manualintegrate((y + 1)**x, x) == x
    y = Symbol('y')
    n = Symbol('n', nonzero=True)
    assert manualintegrate(y**(n*x), x) == Piecewise(
        (y**(n*x)/log(y), Ne(log(y), 0)), (n*x, True))/n
    y = Symbol('y', positive=True)
    assert manualintegrate((y + 1)**(n*x), x) == \
        (y + 1)**(n*x)/(n*log(y + 1))
    a = Symbol('a', negative=True)
    b = Symbol('b')
    assert manualintegrate(1/(a + b*x**2), x) == atan(x/sqrt(a/b))/(b*sqrt(a/b))
    b = Symbol('b', negative=True)
    assert manualintegrate(1/(a + b*x**2), x) == \
        atan(x/(sqrt(-a)*sqrt(-1/b)))/(b*sqrt(-a)*sqrt(-1/b))
    assert manualintegrate(1/((x**a + y**b + 4)*sqrt(a*x**2 + 1)), x) == \
        y**(-b)*Integral(x**(-a)/(y**(-b)*sqrt(a*x**2 + 1) +
        x**(-a)*sqrt(a*x**2 + 1) + 4*x**(-a)*y**(-b)*sqrt(a*x**2 + 1)), x)
    assert manualintegrate(1/((x**2 + 4)*sqrt(4*x**2 + 1)), x) == \
        Integral(1/((x**2 + 4)*sqrt(4*x**2 + 1)), x)
    assert manualintegrate(1/(x - a**x + x*b**2), x) == \
        Integral(1/(-a**x + b**2*x + x), x)

