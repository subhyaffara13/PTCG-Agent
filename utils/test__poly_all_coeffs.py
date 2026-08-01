
def test_Poly_all_coeffs():
    assert Poly(0, x).all_coeffs() == [0]
    assert Poly(1, x).all_coeffs() == [1]

    assert Poly(2*x + 1, x).all_coeffs() == [2, 1]

    assert Poly(7*x**2 + 2*x + 1, x).all_coeffs() == [7, 2, 1]
    assert Poly(7*x**4 + 2*x + 1, x).all_coeffs() == [7, 0, 0, 2, 1]

