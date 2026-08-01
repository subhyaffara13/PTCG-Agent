
def test_puiseux_poly_pow():
    R, x = puiseux_ring('x', QQ)
    Rz, xz = puiseux_ring('x', ZZ)
    assert x**0 == 1 == R({(0,): 1})
    assert x**1 == x == R({(1,): 1})
    assert x**2 == x*x == R({(2,): 1})
    assert x**QQ(1,2) == R({(QQ(1,2),): 1})
    assert x**-1 == 1/x == R({(-1,): 1})
    assert x**-QQ(1,2) == 1/x**QQ(1,2) == R({(-QQ(1,2),): 1})
    assert (2*x)**-1 == 1/(2*x) == QQ(1,2)/x == QQ(1,2)*x**-1 == R({(-1,): QQ(1,2)})
    assert 2/x**2 == 2*x**-2 == R({(-2,): 2})
    assert 2/xz**2 == 2*xz**-2 == Rz({(-2,): 2})
    raises(TypeError, lambda: x**None)
    raises(ValueError, lambda: (x + 1)**-1)
    raises(ValueError, lambda: (x + 1)**QQ(1,2))
    raises(ValueError, lambda: (2*x)**QQ(1,2))
    raises(ValueError, lambda: (2*xz)**-1)

