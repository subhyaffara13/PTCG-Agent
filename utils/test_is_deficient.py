
def test_is_deficient():
    assert is_deficient(10) is True
    assert is_deficient(22) is True
    assert is_deficient(56) is False
    assert is_deficient(20) is False
    assert is_deficient(36) is False

