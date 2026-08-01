
def test_issue_14241():
    x = Symbol('x')
    n = Symbol('n', positive=True, integer=True)
    assert integrate(n * x ** (n - 1) / (x + 1), x) == \
           n**2*x**n*lerchphi(x*exp_polar(I*pi), 1, n)*gamma(n)/gamma(n + 1)

