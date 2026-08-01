
def test_PolyElement_pdiv():
    R, x, y = ring("x,y", ZZ)

    f, g = x**4 + 5*x**3 + 7*x**2, 2*x**2 + 3
    assert f.pdiv(g) == f.pdiv(g, x) == (4*x**2 + 20*x + 22, -60*x - 66)

    f, g = x**2 - y**2, x - y
    assert f.pdiv(g) == f.pdiv(g, 0) == (x + y, 0)

    f, g = x*y + 2*x + 1, x + y
    assert f.pdiv(g) == (y + 2, -y**2 - 2*y + 1)
    assert f.pdiv(g, y) == f.pdiv(g, 1) == (x + 1, -x**2 + 2*x + 1)

    assert R(0).pdiv(g) == (0, 0)
    raises(ZeroDivisionError, lambda: f.prem(R(0)))

