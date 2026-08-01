
def test_numeric_object_coefficients(coefs, tgt):
    p = poly.Polynomial(coefs)
    poly.set_default_printstyle('unicode')
    assert_equal(str(p), tgt)

