
def test_FracElement___call__():
    F, x,y,z = field("x,y,z", ZZ)
    f = (x**2 + 3*y)/z

    r = f(1, 1, 1)
    assert r == 4 and not isinstance(r, FracElement)
    raises(ZeroDivisionError, lambda: f(1, 1, 0))

