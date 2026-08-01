
def test_business_daily_look_alike():
    # see gh-16624
    #
    # Do not infer "B when "weekend" (2-day gap) in wrong place.
    index = DatetimeIndex(["12/31/1998", "1/3/1999", "1/4/1999"])
    assert frequencies.infer_freq(index) is None

