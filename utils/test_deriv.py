
def test_deriv(Poly):
    # Check that the derivative is the inverse of integration. It is
    # assumes that the integration has been checked elsewhere.
    d = Poly.domain + random((2,)) * .25
    w = Poly.window + random((2,)) * .25
    p1 = Poly([1, 2, 3], domain=d, window=w)
    p2 = p1.integ(2, k=[1, 2])
    p3 = p1.integ(1, k=[1])
    assert_almost_equal(p2.deriv(1).coef, p3.coef)
    assert_almost_equal(p2.deriv(2).coef, p1.coef)
    # default domain and window
    p1 = Poly([1, 2, 3])
    p2 = p1.integ(2, k=[1, 2])
    p3 = p1.integ(1, k=[1])
    assert_almost_equal(p2.deriv(1).coef, p3.coef)
    assert_almost_equal(p2.deriv(2).coef, p1.coef)

