
def test_polyval():
    assert polyval([], 3) == 0
    assert polyval([0], 3) == 0
    assert polyval([5], 3) == 5
    # 4x^3 - 2x + 5
    p = [4, 0, -2, 5]
    assert polyval(p,4) == 253
    assert polyval(p,4,derivative=True) == (253, 190)

