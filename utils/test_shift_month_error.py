
def test_shift_month_error():
    dt = datetime(2017, 11, 15)
    day_opt = "this should raise"

    with pytest.raises(ValueError, match=day_opt):
        liboffsets.shift_month(dt, 3, day_opt=day_opt)

