
def test_to_rational_coeffs():
    assert to_rational_coeffs(
        Poly(x**3 + y*x**2 + sqrt(y), x, domain='EX')) is None
    # issue 21268
    assert to_rational_coeffs(
        Poly(y**3 + sqrt(2)*y**2*sin(x) + 1, y)) is None

    assert to_rational_coeffs(Poly(x, y)) is None
    assert to_rational_coeffs(Poly(sqrt(2)*y)) is None

