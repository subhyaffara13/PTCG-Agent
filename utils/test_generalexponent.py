
def test_generalexponent():
    p = 2
    e = (2/x + 3/x**p)/(1/x + 1/x**p)
    assert e.nseries(x, 0, 3) == 3 - x + x**2 + O(x**3)
    p = S.Half
    e = (2/x + 3/x**p)/(1/x + 1/x**p)
    assert e.nseries(x, 0, 2) == 2 - x + sqrt(x) + x**(S(3)/2) + O(x**2)

    e = 1 + sqrt(x)
    assert e.nseries(x, 0, 4) == 1 + sqrt(x)

