
def test_expsinbug():
    assert exp(sin(x)).series(x, 0, 0) == O(1, x)
    assert exp(sin(x)).series(x, 0, 1) == 1 + O(x)
    assert exp(sin(x)).series(x, 0, 2) == 1 + x + O(x**2)
    assert exp(sin(x)).series(x, 0, 3) == 1 + x + x**2/2 + O(x**3)
    assert exp(sin(x)).series(x, 0, 4) == 1 + x + x**2/2 + O(x**4)
    assert exp(sin(x)).series(x, 0, 5) == 1 + x + x**2/2 - x**4/8 + O(x**5)

