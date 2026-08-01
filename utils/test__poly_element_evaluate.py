
def test_PolyElement_evaluate():
    R, x = ring("x", ZZ)
    f = x**3 + 4*x**2 + 2*x + 3

    r = f.evaluate(x, 0)
    assert r == 3 and not isinstance(r, PolyElement)

    raises(CoercionFailed, lambda: f.evaluate(x, QQ(1,7)))

    R, x, y, z = ring("x,y,z", ZZ)
    f = (x*y)**3 + 4*(x*y)**2 + 2*x*y + 3

    r = f.evaluate(x, 0)
    assert r == 3 and R.drop(x).is_element(r)
    r = f.evaluate([(x, 0), (y, 0)])
    assert r == 3 and R.drop(x, y).is_element(r)
    r = f.evaluate(y, 0)
    assert r == 3 and R.drop(y).is_element(r)
    r = f.evaluate([(y, 0), (x, 0)])
    assert r == 3 and R.drop(y, x).is_element(r)

    r = f.evaluate([(x, 0), (y, 0), (z, 0)])
    assert r == 3 and not isinstance(r, PolyElement)

    raises(CoercionFailed, lambda: f.evaluate([(x, 1), (y, QQ(1,7))]))
    raises(CoercionFailed, lambda: f.evaluate([(x, QQ(1,7)), (y, 1)]))
    raises(CoercionFailed, lambda: f.evaluate([(x, QQ(1,7)), (y, QQ(1,7))]))

