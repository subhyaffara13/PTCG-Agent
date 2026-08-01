
def test_PolyElement_pexquo():
    R, x, y = ring("x, y", ZZ)

    f, g = x**2 - y**2, x - y
    assert f.pexquo(g) == f.pexquo(g, x) == x + y
    assert f.pexquo(g, y) == f.pexquo(g, 1) == x + y + 1

    f, g = x**2 + 3*x + 6, x + 2
    raises(ExactQuotientFailed, lambda: f.pexquo(g))

