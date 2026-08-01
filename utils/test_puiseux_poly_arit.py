
def test_puiseux_poly_arit():
    R, x = puiseux_ring('x', QQ)
    R2, y = puiseux_ring('y', QQ)
    p = x**2 + 1
    assert +p == p
    assert -p == -1 - x**2
    assert p + p == 2*p == 2*x**2 + 2
    assert p + 1 == 1 + p == x**2 + 2
    assert p + QQ(1,2) == QQ(1,2) + p == x**2 + QQ(3,2)
    assert p - p == 0
    assert p - 1 == -1 + p == x**2
    assert p - QQ(1,2) == -QQ(1,2) + p == x**2 + QQ(1,2)
    assert 1 - p == -p + 1 == -x**2
    assert QQ(1,2) - p == -p + QQ(1,2) == -x**2 - QQ(1,2)
    assert p * p == x**4 + 2*x**2 + 1
    assert p * 1 == 1 * p == p
    assert 2 * p == p * 2 == 2*x**2 + 2
    assert p * QQ(1,2) == QQ(1,2) * p == QQ(1,2)*x**2 + QQ(1,2)
    assert x**QQ(1,2) * x**QQ(1,2) == x
    raises(ValueError, lambda: x + y)
    raises(ValueError, lambda: x - y)
    raises(ValueError, lambda: x * y)
    raises(TypeError, lambda: x + None)
    raises(TypeError, lambda: x - None)
    raises(TypeError, lambda: x * None)
    raises(TypeError, lambda: None + x)
    raises(TypeError, lambda: None - x)
    raises(TypeError, lambda: None * x)

