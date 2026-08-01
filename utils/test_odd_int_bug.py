
def test_odd_int_bug():
    assert to_int(from_int(3), round_nearest) == 3

