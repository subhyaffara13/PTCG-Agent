
def test_issue_24210_25885():
    eq = exp(x)/(1+1/x)**x**2
    ans = sqrt(E)
    assert gruntz(eq, x, oo) == ans
    assert gruntz(1/eq, x, oo) == 1/ans

