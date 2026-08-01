
def test_log_series():
    l = Symbol('l')
    e = 1/(1 - log(x))
    assert e.nseries(x, n=5, logx=l) == 1/(1 - l)


def test_log_series():
    # Note Series at infinities other than oo/-oo were introduced as a part of
    # pull request 23798. Refer https://github.com/sympy/sympy/pull/23798 for
    # more information.
    expr1 = log(1 + x)
    expr2 = log(x + sqrt(x**2 + 1))

    assert expr1.series(x, x0=I*oo, n=4) == 1/(3*x**3) - 1/(2*x**2) + 1/x + \
    I*pi/2 - log(I/x) + O(x**(-4), (x, oo*I))
    assert expr1.series(x, x0=-I*oo, n=4) == 1/(3*x**3) - 1/(2*x**2) + 1/x - \
    I*pi/2 - log(-I/x) + O(x**(-4), (x, -oo*I))
    assert expr2.series(x, x0=I*oo, n=4) == 1/(4*x**2) + I*pi/2 + log(2) - \
    log(I/x) + O(x**(-4), (x, oo*I))
    assert expr2.series(x, x0=-I*oo, n=4) == -1/(4*x**2) - I*pi/2 - log(2) + \
    log(-I/x) + O(x**(-4), (x, -oo*I))

