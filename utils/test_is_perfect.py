
def test_is_perfect():
    assert is_perfect(-6) is False
    assert is_perfect(6) is True
    assert is_perfect(15) is False
    assert is_perfect(28) is True
    assert is_perfect(400) is False
    assert is_perfect(496) is True
    assert is_perfect(8128) is True
    assert is_perfect(10000) is False

