
def test_T1():
    assert limit((1 + 1/n)**n, n, oo) == E
    assert limit((1 - cos(x))/x**2, x, 0) == S.Half

