
def test_fifth_week_of_month_infer():
    # see gh-9425
    #
    # Only attempt to infer up to WOM-4.
    index = DatetimeIndex(["2014-03-31", "2014-06-30", "2015-03-30"])
    assert frequencies.infer_freq(index) is None

