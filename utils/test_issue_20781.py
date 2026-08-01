
def test_issue_20781():
    P = lambda a: Piecewise((0, x < a), (1, x >= a))
    f = lambda a: P(int(a)) + P(float(a))
    L = (x, -float('Inf'), x)
    f1 = integrate(f(1), L)
    assert f1 == 2*x - Min(1.0, x) - Min(x, Max(1.0, 1, evaluate=False))
    # XXX is_zero is True for S(0) and Float(0) and this is baked into
    # the code more deeply than the issue of Float(0) != S(0)
    assert integrate(f(0), (x, -float('Inf'), x)
        ) == 2*x - 2*Min(0, x)

