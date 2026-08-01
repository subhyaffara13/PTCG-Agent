
def test_Poly_abs():
    assert Poly(-x + 1, x).abs() == abs(Poly(-x + 1, x)) == Poly(x + 1, x)

