
def test_regular_point():
    r1 = ImplicitRegion((x,), x**2 - 16)
    assert r1.regular_point() == (-4,)
    c1 = ImplicitRegion((x, y), x**2 + y**2 - 4)
    assert c1.regular_point() == (0, -2)
    c2 = ImplicitRegion((x, y), (x - S(5)/2)**2 + y**2 - (S(1)/4)**2)
    assert c2.regular_point() == (S(5)/2, -S(1)/4)
    c3 = ImplicitRegion((x, y), (y - 5)**2  - 16*(x - 5))
    assert c3.regular_point() == (5, 5)
    r2 = ImplicitRegion((x, y), x**2 - 4*x*y - 3*y**2 + 4*x + 8*y - 5)
    assert r2.regular_point() == (S(4)/7, S(9)/7)
    r3 = ImplicitRegion((x, y), x**2 - 2*x*y + 3*y**2 - 2*x - 5*y + 3/2)
    raises(ValueError, lambda: r3.regular_point())

