
def test_degree(Poly):
    p = Poly.basis(5)
    assert_equal(p.degree(), 5)

