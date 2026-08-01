
def test_get_day_of_month_error():
    # get_day_of_month is not directly exposed.
    # We test it via roll_qtrday.
    dt = datetime(2017, 11, 15)
    day_opt = "foo"

    with pytest.raises(ValueError, match=day_opt):
        # To hit the raising case we need month == dt.month and n > 0.
        roll_qtrday(dt, n=3, month=11, day_opt=day_opt, modby=12)

