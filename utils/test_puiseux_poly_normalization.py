
def test_puiseux_poly_normalization():
    R, x = puiseux_ring('x', QQ)
    assert (x**2 + 1) / x == x + 1/x == R({(1,): 1, (-1,): 1})
    assert (x**QQ(1,6))**2 == x**QQ(1,3) == R({(QQ(1,3),): 1})
    assert (x**QQ(1,6))**(-2) == x**(-QQ(1,3)) == R({(-QQ(1,3),): 1})
    assert (x**QQ(1,6))**QQ(1,2) == x**QQ(1,12) == R({(QQ(1,12),): 1})
    assert (x**QQ(1,6))**6 == x == R({(1,): 1})
    assert x**QQ(1,6) * x**QQ(1,3) == x**QQ(1,2) == R({(QQ(1,2),): 1})
    assert 1/x * x**2 == x == R({(1,): 1})
    assert 1/x**QQ(1,3) * x**QQ(1,3) == 1 == R({(0,): 1})

