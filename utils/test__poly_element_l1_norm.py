
def test_PolyElement_l1_norm():
    R, x, y = ring("x,y", ZZ)

    assert R(0).l1_norm() == 0
    assert R(1).l1_norm() == 1

    assert (x**3 + 4*x**2 + 2*x + 3).l1_norm() == 10

