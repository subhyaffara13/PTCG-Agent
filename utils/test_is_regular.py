
def test_is_regular():
    R, x, y = puiseux_ring('x, y', QQ)
    p = 1 + 2*x + x**2 + 3*x**3
    assert not rs_is_puiseux(p, x)

    p = x + x**QQ(1,5)*y
    assert rs_is_puiseux(p, x)
    assert not rs_is_puiseux(p, y)

    p = x + x**2*y**QQ(1,5)*y
    assert not rs_is_puiseux(p, x)

