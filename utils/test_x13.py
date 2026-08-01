
def test_X13():
    assert series(sqrt(2*x**2 + 1), x, x0=oo, n=1) == sqrt(2)*x + O(1/x, (x, oo))

