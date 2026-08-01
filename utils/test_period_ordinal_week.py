
def test_period_ordinal_week(dt, expected):
    args = (*dt, get_freq_code("W"))
    assert period_ordinal(*args) == expected

