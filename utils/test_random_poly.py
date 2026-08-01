
def test_random_poly():
    poly = random_poly(x, 10, -100, 100, polys=False)

    assert Poly(poly).degree() == 10
    assert all(-100 <= coeff <= 100 for coeff in Poly(poly).coeffs()) is True

    poly = random_poly(x, 10, -100, 100, polys=True)

    assert poly.degree() == 10
    assert all(-100 <= coeff <= 100 for coeff in poly.coeffs()) is True

