
def test_PolyElement_subs():
    R, x = ring("x", ZZ)
    f = x**3 + 4*x**2 + 2*x + 3

    r = f.subs(x, 0)
    assert r == 3 and R.is_element(r)

    raises(CoercionFailed, lambda: f.subs(x, QQ(1,7)))

    R, x, y, z = ring("x,y,z", ZZ)
    f = x**3 + 4*x**2 + 2*x + 3

    r = f.subs(x, 0)
    assert r == 3 and R.is_element(r)
    r = f.subs([(x, 0), (y, 0)])
    assert r == 3 and R.is_element(r)

    raises(CoercionFailed, lambda: f.subs([(x, 1), (y, QQ(1,7))]))
    raises(CoercionFailed, lambda: f.subs([(x, QQ(1,7)), (y, 1)]))
    raises(CoercionFailed, lambda: f.subs([(x, QQ(1,7)), (y, QQ(1,7))]))

