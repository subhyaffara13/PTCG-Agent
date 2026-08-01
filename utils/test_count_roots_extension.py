
def test_count_roots_extension():

    p1 = Poly(sqrt(2)*x**2 - 2, x, extension=True)
    assert p1.count_roots() == 2
    assert p1.count_roots(inf=0) == 1
    assert p1.count_roots(sup=0) == 1

    p2 = Poly(x**2 + sqrt(2), x, extension=True)
    assert p2.count_roots() == 0

    p3 = Poly(x**2 + 2*sqrt(2)*x + 1, x, extension=True)
    assert p3.count_roots() == 2
    assert p3.count_roots(inf=-10, sup=10) == 2
    assert p3.count_roots(inf=-10, sup=0) == 2
    assert p3.count_roots(inf=-10, sup=-3) == 0
    assert p3.count_roots(inf=-3, sup=-2) == 1
    assert p3.count_roots(inf=-1, sup=0) == 1

