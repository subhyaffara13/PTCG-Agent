
def test_issue_3623():
    assert integrate(cos((n + 1)*x), x) == Piecewise(
        (sin(x*(n + 1))/(n + 1), Ne(n + 1, 0)), (x, True))
    assert integrate(cos((n - 1)*x), x) == Piecewise(
        (sin(x*(n - 1))/(n - 1), Ne(n - 1, 0)), (x, True))
    assert integrate(cos((n + 1)*x) + cos((n - 1)*x), x) == \
        Piecewise((sin(x*(n - 1))/(n - 1), Ne(n - 1, 0)), (x, True)) + \
        Piecewise((sin(x*(n + 1))/(n + 1), Ne(n + 1, 0)), (x, True))

