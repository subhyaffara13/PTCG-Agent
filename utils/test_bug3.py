
def test_bug3():
    e = (2/x + 3/x**2)/(1/x + 1/x**2)
    assert e.nseries(x, n=3) == 3 - x + x**2 + O(x**3)


def test_bug3():
    a = Symbol("a")
    b = Symbol("b", positive=True)
    e = 2*a + b
    f = b + 2*a
    assert e == f

