
def test_nonnumeric_object_coefficients(coefs, tgt):
    """
    Test coef fallback for object arrays of non-numeric coefficients.
    """
    p = poly.Polynomial(coefs)
    poly.set_default_printstyle('unicode')
    assert_equal(str(p), tgt)

