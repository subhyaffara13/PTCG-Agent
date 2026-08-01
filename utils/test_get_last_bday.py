
def test_get_last_bday(dt, exp_week_day, exp_last_day):
    assert dt.weekday() == exp_week_day
    assert get_lastbday(dt.year, dt.month) == exp_last_day

