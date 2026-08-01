
def test_find_carmichael_numbers_in_range():
    assert find_carmichael_numbers_in_range(0, 561) == []
    assert find_carmichael_numbers_in_range(561, 562) == [561]
    assert find_carmichael_numbers_in_range(561, 1105) == find_carmichael_numbers_in_range(561, 562)
    raises(ValueError, lambda: find_carmichael_numbers_in_range(-2, 2))
    raises(ValueError, lambda: find_carmichael_numbers_in_range(22, 2))

