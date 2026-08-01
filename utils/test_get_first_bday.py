
def test_get_first_bday(dt, exp_week_day, exp_first_day):
    assert dt.weekday() == exp_week_day
    assert get_firstbday(dt.year, dt.month) == exp_first_day

