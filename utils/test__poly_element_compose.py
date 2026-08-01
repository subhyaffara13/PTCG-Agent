
def test_PolyElement_compose():
    R, x = ring("x", ZZ)
    f = x**3 + 4*x**2 + 2*x + 3

    r = f.compose(x, 0)
    assert r == 3 and R.is_element(r)

    assert f.compose(x, x) == f
    assert f.compose(x, x**2) == x**6 + 4*x**4 + 2*x**2 + 3

    raises(CoercionFailed, lambda: f.compose(x, QQ(1,7)))

    R, x, y, z = ring("x,y,z", ZZ)
    f = x**3 + 4*x**2 + 2*x + 3

    r = f.compose(x, 0)
    assert r == 3 and R.is_element(r)
    r = f.compose([(x, 0), (y, 0)])
    assert r == 3 and R.is_element(r)

    r = (x**3 + 4*x**2 + 2*x*y*z + 3).compose(x, y*z**2 - 1)
    q = (y*z**2 - 1)**3 + 4*(y*z**2 - 1)**2 + 2*(y*z**2 - 1)*y*z + 3
    assert r == q and R.is_element(r)

