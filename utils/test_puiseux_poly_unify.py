
def test_puiseux_poly_unify():
    R, x = puiseux_ring('x', QQ)
    assert 1/x + x == x + 1/x == R({(1,): 1, (-1,): 1})
    assert repr(1/x + x) == 'x**(-1) + x'
    assert 1/x + 1/x == 2/x == R({(-1,): 2})
    assert repr(1/x + 1/x) == '2*x**(-1)'
    assert x**QQ(1,2) + x**QQ(1,2) == 2*x**QQ(1,2) == R({(QQ(1,2),): 2})
    assert repr(x**QQ(1,2) + x**QQ(1,2)) == '2*x**(1/2)'
    assert x**QQ(1,2) + x**QQ(1,3) == R({(QQ(1,2),): 1, (QQ(1,3),): 1})
    assert repr(x**QQ(1,2) + x**QQ(1,3)) == 'x**(1/3) + x**(1/2)'
    assert x + x**QQ(1,2) == R({(1,): 1, (QQ(1,2),): 1})
    assert repr(x + x**QQ(1,2)) == 'x**(1/2) + x'
    assert 1/x**QQ(1,2) + 1/x**QQ(1,3) == R({(-QQ(1,2),): 1, (-QQ(1,3),): 1})
    assert repr(1/x**QQ(1,2) + 1/x**QQ(1,3)) == 'x**(-1/2) + x**(-1/3)'
    assert 1/x + x**QQ(1,2) == x**QQ(1,2) + 1/x == R({(-1,): 1, (QQ(1,2),): 1})
    assert repr(1/x + x**QQ(1,2)) == 'x**(-1) + x**(1/2)'

