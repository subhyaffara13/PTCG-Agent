import random

def test_basis(Poly):
    d = Poly.domain + random((2,)) * .25
    w = Poly.window + random((2,)) * .25
    p = Poly.basis(5, domain=d, window=w)
    assert_equal(p.domain, d)
    assert_equal(p.window, w)
    assert_equal(p.coef, [0] * 5 + [1])


def test_basis():
    p = poly.Polynomial.basis(3, symbol='z')
    assert_equal(p.symbol, 'z')

