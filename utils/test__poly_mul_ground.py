
def test_Poly_mul_ground():
    assert Poly(x + 1).mul_ground(2) == Poly(2*x + 2)

