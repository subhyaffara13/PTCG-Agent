
def test_issue_14129():
    x = Symbol('x', zero=False)
    assert Sum( k*x**k, (k, 0, n-1)).doit() == \
        Piecewise((n**2/2 - n/2, Eq(x, 1)), ((n*x*x**n -
            n*x**n - x*x**n + x)/(x - 1)**2, True))
    assert Sum( x**k, (k, 0, n-1)).doit() == \
        Piecewise((n, Eq(x, 1)), ((-x**n + 1)/(-x + 1), True))
    assert Sum( k*(x/y+x)**k, (k, 0, n-1)).doit() == \
        Piecewise((n*(n - 1)/2, Eq(x, y/(y + 1))),
        (x*(y + 1)*(n*x*y*(x + x/y)**(n - 1) +
        n*x*(x + x/y)**(n - 1) - n*y*(x + x/y)**(n - 1) -
        x*y*(x + x/y)**(n - 1) - x*(x + x/y)**(n - 1) + y)/
        (x*y + x - y)**2, True))

