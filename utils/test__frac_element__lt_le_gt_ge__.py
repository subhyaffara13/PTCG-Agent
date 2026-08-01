
def test_FracElement__lt_le_gt_ge__():
    F, x, y = field("x,y", ZZ)

    assert F(1) < 1/x < 1/x**2 < 1/x**3
    assert F(1) <= 1/x <= 1/x**2 <= 1/x**3

    assert -7/x < 1/x < 3/x < y/x < 1/x**2
    assert -7/x <= 1/x <= 3/x <= y/x <= 1/x**2

    assert 1/x**3 > 1/x**2 > 1/x > F(1)
    assert 1/x**3 >= 1/x**2 >= 1/x >= F(1)

    assert 1/x**2 > y/x > 3/x > 1/x > -7/x
    assert 1/x**2 >= y/x >= 3/x >= 1/x >= -7/x

