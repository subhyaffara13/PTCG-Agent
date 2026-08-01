
def test_subs_AccumBounds():
    e = x
    e = e.subs(x, AccumBounds(1, 3))
    assert e == AccumBounds(1, 3)

    e = 2*x
    e = e.subs(x, AccumBounds(1, 3))
    assert e == AccumBounds(2, 6)

    e = x + x**2
    e = e.subs(x, AccumBounds(-1, 1))
    assert e == AccumBounds(-1, 2)

