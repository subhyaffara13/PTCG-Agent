
def test_PolyElement__lt_le_gt_ge__():
    R, x, y = ring("x,y", ZZ)

    assert R(1) < x < x**2 < x**3
    assert R(1) <= x <= x**2 <= x**3

    assert x**3 > x**2 > x > R(1)
    assert x**3 >= x**2 >= x >= R(1)

