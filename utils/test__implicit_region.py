
def test_ImplicitRegion():
    ellipse = ImplicitRegion((x, y), (x**2/4 + y**2/16 - 1))
    assert ellipse.equation == x**2/4 + y**2/16 - 1
    assert ellipse.variables == (x, y)
    assert ellipse.degree == 2
    r = ImplicitRegion((x, y, z), Eq(x**4 + y**2 - x*y, 6))
    assert r.equation == x**4 + y**2 - x*y - 6
    assert r.variables == (x, y, z)
    assert r.degree == 4

