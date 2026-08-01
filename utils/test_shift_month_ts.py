
def test_shift_month_ts(months, day_opt, expected):
    ts = Timestamp("1929-05-05")
    assert liboffsets.shift_month(ts, months, day_opt=day_opt) == expected

