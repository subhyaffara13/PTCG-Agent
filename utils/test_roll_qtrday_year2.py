
def test_roll_qtrday_year2(other, expected, n):
    month = 6
    day_opt = "end"  # `other` will be compared to June 30.

    assert roll_qtrday(other, n, month, day_opt, modby=12) == expected[n]

