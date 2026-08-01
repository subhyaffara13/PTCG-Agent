
def test_apply_ticks():
    result = offsets.Hour(3) + offsets.Hour(4)
    exp = offsets.Hour(7)
    assert result == exp

