
def test_shift_month_dt(months, day_opt, expected):
    dt = datetime(2017, 11, 30)
    assert liboffsets.shift_month(dt, months, day_opt=day_opt) == expected

