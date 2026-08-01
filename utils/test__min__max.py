
def test_Min_Max():
    # see gh-10375
    assert lambdify((x, y, z), Min(x, y, z))(1, 2, 3) == 1
    assert lambdify((x, y, z), Max(x, y, z))(1, 2, 3) == 3

