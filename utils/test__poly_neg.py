
def test_Poly_neg():
    assert Poly(-x + 1, x).neg() == -Poly(-x + 1, x) == Poly(x - 1, x)

