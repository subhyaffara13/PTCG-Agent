
def test_integ(Poly):
    P = Polynomial
    # Check defaults
    p0 = Poly.cast(P([1 * 2, 2 * 3, 3 * 4]))
    p1 = P.cast(p0.integ())
    p2 = P.cast(p0.integ(2))
    assert_poly_almost_equal(p1, P([0, 2, 3, 4]))
    assert_poly_almost_equal(p2, P([0, 0, 1, 1, 1]))
    # Check with k
    p0 = Poly.cast(P([1 * 2, 2 * 3, 3 * 4]))
    p1 = P.cast(p0.integ(k=1))
    p2 = P.cast(p0.integ(2, k=[1, 1]))
    assert_poly_almost_equal(p1, P([1, 2, 3, 4]))
    assert_poly_almost_equal(p2, P([1, 1, 1, 1, 1]))
    # Check with lbnd
    p0 = Poly.cast(P([1 * 2, 2 * 3, 3 * 4]))
    p1 = P.cast(p0.integ(lbnd=1))
    p2 = P.cast(p0.integ(2, lbnd=1))
    assert_poly_almost_equal(p1, P([-9, 2, 3, 4]))
    assert_poly_almost_equal(p2, P([6, -9, 1, 1, 1]))
    # Check scaling
    d = 2 * Poly.domain
    p0 = Poly.cast(P([1 * 2, 2 * 3, 3 * 4]), domain=d)
    p1 = P.cast(p0.integ())
    p2 = P.cast(p0.integ(2))
    assert_poly_almost_equal(p1, P([0, 2, 3, 4]))
    assert_poly_almost_equal(p2, P([0, 0, 1, 1, 1]))

