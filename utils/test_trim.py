
def test_trim(Poly):
    c = [1, 1e-6, 1e-12, 0]
    p = Poly(c)
    assert_equal(p.trim().coef, c[:3])
    assert_equal(p.trim(1e-10).coef, c[:2])
    assert_equal(p.trim(1e-5).coef, c[:1])

