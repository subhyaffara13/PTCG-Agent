
def test_puiseux_poly_repr():
    R, x = puiseux_ring('x', QQ)
    assert repr(x) == 'x'
    assert repr(x**QQ(1,2)) == 'x**(1/2)'
    assert repr(1/x) == 'x**(-1)'
    assert repr(2*x**2 + 1) == '1 + 2*x**2'
    assert repr(R.one) == '1'
    assert repr(2*R.one) == '2'

