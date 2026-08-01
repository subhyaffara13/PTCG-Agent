
def test_roll_qtrday_year(other, expected, n):
    month = 3
    day_opt = "start"  # `other` will be compared to March 1.

    assert roll_qtrday(other, n, month, day_opt, modby=12) == expected[n]

