
def test_pr_22677():
    b = Symbol('b', integer=True, positive=True)
    assert Sum(1/x**2,(x, 0, b)).doit() == Sum(x**(-2), (x, 0, b))
    assert Sum(1/(x - b)**2,(x, 0, b-1)).doit() == Sum(
        (-b + x)**(-2), (x, 0, b - 1))

