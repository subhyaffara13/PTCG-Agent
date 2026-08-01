
def test_PolyElement_prem():
    R, x, y = ring("x, y", ZZ)

    f, g = x**2 + x*y, 2*x + 2
    assert f.prem(g) == -4*y + 4 # first generator is chosen by default if it is not given

    f, g = x**2 + 1, 2*x - 4
    assert f.prem(g) == f.prem(g, x) == 20
    assert f.prem(g, 1) == R(0)

    f, g = x*y + 2*x + 1, x + y
    assert f.prem(g) == -y**2 - 2*y + 1
    assert f.prem(g, 1) == f.prem(g, y) == -x**2 + 2*x + 1

    raises(ZeroDivisionError, lambda: f.prem(R(0)))

