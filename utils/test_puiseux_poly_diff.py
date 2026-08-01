
def test_puiseux_poly_diff():
    R, x, y = puiseux_ring('x, y', QQ)
    assert (x**2 + 1).diff(x) == 2*x
    assert (x**2 + 1).diff(y) == 0
    assert (x**2 + y**2).diff(x) == 2*x
    assert (x**QQ(1,2) + y**QQ(1,2)).diff(x) == QQ(1,2)*x**-QQ(1,2)
    assert ((x*y)**QQ(1,2)).diff(x) == QQ(1,2)*y**QQ(1,2)*x**-QQ(1,2)

