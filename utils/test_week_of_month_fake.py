
def test_week_of_month_fake():
    # All of these dates are on same day
    # of week and are 4 or 5 weeks apart.
    index = DatetimeIndex(["2013-08-27", "2013-10-01", "2013-10-29", "2013-11-26"])
    assert frequencies.infer_freq(index) != "WOM-4TUE"

