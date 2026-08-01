
def test_puiseux_poly_div():
    R, x = puiseux_ring('x', QQ)
    R2, y = puiseux_ring('y', QQ)
    p = x**2 - 1
    assert p / 1 == p
    assert p / QQ(1,2) == 2*p == 2*x**2 - 2
    assert p / x == x - 1/x == R({(1,): 1, (-1,): -1})
    assert 2 / x == 2*x**-1 == R({(-1,): 2})
    assert QQ(1,2) / x == QQ(1,2)*x**-1 == 1/(2*x) == 1/x/2 == R({(-1,): QQ(1,2)})
    raises(ZeroDivisionError, lambda: p / 0)
    raises(ValueError, lambda: (x + 1) / (x + 2))
    raises(ValueError, lambda: (x + 1) / (x + 1))
    raises(ValueError, lambda: x / y)
    raises(TypeError, lambda: x / None)
    raises(TypeError, lambda: None / x)

