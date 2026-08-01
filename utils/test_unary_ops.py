
def test_unary_ops():
    assert +NA is NA
    assert -NA is NA
    assert abs(NA) is NA
    assert ~NA is NA

