
def test_is_zero_dimensional():
    assert is_zero_dimensional([x, y], x, y) is True
    assert is_zero_dimensional([x**3 + y**2], x, y) is False

    assert is_zero_dimensional([x, y, z], x, y, z) is True
    assert is_zero_dimensional([x, y, z], x, y, z, t) is False

    F = [x*y - z, y*z - x, x*y - y]
    assert is_zero_dimensional(F, x, y, z) is True

    F = [x**2 - 2*x*z + 5, x*y**2 + y*z**3, 3*y**2 - 8*z**2]
    assert is_zero_dimensional(F, x, y, z) is True

