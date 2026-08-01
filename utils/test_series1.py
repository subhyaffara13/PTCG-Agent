
def test_series1():
    e = sin(x)
    assert e.nseries(x, 0, 0) != 0
    assert e.nseries(x, 0, 0) == O(1, x)
    assert e.nseries(x, 0, 1) == O(x, x)
    assert e.nseries(x, 0, 2) == x + O(x**2, x)
    assert e.nseries(x, 0, 3) == x + O(x**3, x)
    assert e.nseries(x, 0, 4) == x - x**3/6 + O(x**4, x)

    e = (exp(x) - 1)/x
    assert e.nseries(x, 0, 3) == 1 + x/2 + x**2/6 + O(x**3)

    assert x.nseries(x, 0, 2) == x

