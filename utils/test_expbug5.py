
def test_expbug5():
    assert exp(log(1 + x)/x).nseries(x, n=3) == exp(1) + -exp(1)*x/2 + 11*exp(1)*x**2/24 + O(x**3)

    assert exp(O(x)).nseries(x, 0, 2) == 1 + O(x)

