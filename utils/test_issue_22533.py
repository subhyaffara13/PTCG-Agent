
def test_issue_22533():
    x = Symbol('x', real=True)
    f = Piecewise((-1 / x, x <= 0), (1 / x, True))
    assert integrate(f, x) == Piecewise((-log(x), x <= 0), (log(x), True))

