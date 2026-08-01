
def test_complex_coefficients():
    """Test both numpy and built-in complex."""
    coefs = [0 + 1j, 1 + 1j, -2 + 2j, 3 + 0j]
    # numpy complex
    p1 = poly.Polynomial(coefs)
    # Python complex
    p2 = poly.Polynomial(array(coefs, dtype=object))
    poly.set_default_printstyle('unicode')
    assert_equal(str(p1), "1j + (1+1j)·x - (2-2j)·x² + (3+0j)·x³")
    assert_equal(str(p2), "1j + (1+1j)·x + (-2+2j)·x² + (3+0j)·x³")
    poly.set_default_printstyle('ascii')
    assert_equal(str(p1), "1j + (1+1j) x - (2-2j) x**2 + (3+0j) x**3")
    assert_equal(str(p2), "1j + (1+1j) x + (-2+2j) x**2 + (3+0j) x**3")

