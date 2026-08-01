
def test_evalf_symbolic():
    # issue 6328
    expr = Sum(f(x), (x, 1, 3)) + Sum(g(x), (x, 1, 3))
    assert expr.evalf() == expr

