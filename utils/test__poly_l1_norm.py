
def test_Poly_l1_norm():
    assert Poly(-1, x).l1_norm() == 1
    assert Poly( 0, x).l1_norm() == 0
    assert Poly( 1, x).l1_norm() == 1

