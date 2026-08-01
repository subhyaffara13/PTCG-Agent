
def test_issue_7827():
    x, n, M = symbols('x n M')
    N = Symbol('N', integer=True)
    assert integrate(summation(x*n, (n, 1, N)), x) == x**2*(N**2/4 + N/4)
    assert integrate(summation(x*sin(n), (n,1,N)), x) == \
        Sum(x**2*sin(n)/2, (n, 1, N))
    assert integrate(summation(sin(n*x), (n,1,N)), x) == \
        Sum(Piecewise((-cos(n*x)/n, Ne(n, 0)), (0, True)), (n, 1, N))
    assert integrate(integrate(summation(sin(n*x), (n,1,N)), x), x) == \
        Piecewise((Sum(Piecewise((-sin(n*x)/n**2, Ne(n, 0)), (-x/n, True)),
        (n, 1, N)), (n > -oo) & (n < oo) & Ne(n, 0)), (0, True))
    assert integrate(Sum(x, (n, 1, M)), x) == M*x**2/2
    raises(ValueError, lambda: integrate(Sum(x, (x, y, n)), y))
    raises(ValueError, lambda: integrate(Sum(x, (x, 1, n)), n))
    raises(ValueError, lambda: integrate(Sum(x, (x, 1, y)), x))

