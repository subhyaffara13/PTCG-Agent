
def test_issue_24276():
    fx = log(tan(pi/2*tanh(x))).diff(x)
    assert fx.limit(x, oo) == 2
    assert fx.simplify().limit(x, oo) == 2
    assert fx.rewrite(sin).limit(x, oo) == 2
    assert fx.rewrite(sin).simplify().limit(x, oo) == 2

