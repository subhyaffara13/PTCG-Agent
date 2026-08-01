
def test_PolyElement_pquo():
    R, x, y = ring("x, y", ZZ)

    f, g = x**4 - 4*x**2*y + 4*y**2, x**2 - 2*y
    assert f.pquo(g) == f.pquo(g, x) == x**2 - 2*y
    assert f.pquo(g, y) == 4*x**2 - 8*y + 4

    f, g = x**4 - y**4, x**2 - y**2
    assert f.pquo(g) == f.pquo(g, 0) == x**2 + y**2

