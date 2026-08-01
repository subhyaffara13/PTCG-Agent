
def test_fromroots(Poly):
    # check that requested roots are zeros of a polynomial
    # of correct degree, domain, and window.
    d = Poly.domain + random((2,)) * .25
    w = Poly.window + random((2,)) * .25
    r = random((5,))
    p1 = Poly.fromroots(r, domain=d, window=w)
    assert_equal(p1.degree(), len(r))
    assert_equal(p1.domain, d)
    assert_equal(p1.window, w)
    assert_almost_equal(p1(r), 0)

    # check that polynomial is monic
    pdom = Polynomial.domain
    pwin = Polynomial.window
    p2 = Polynomial.cast(p1, domain=pdom, window=pwin)
    assert_almost_equal(p2.coef[-1], 1)

