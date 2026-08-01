
def test_RootOf_is_imaginary():
    r = RootOf(x**4 + 4*x**2 + 1, 1)
    i = r._get_interval()
    assert r.is_imaginary and i.ax*i.bx <= 0

