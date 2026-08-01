
def test_business_daily():
    index = DatetimeIndex(["01/01/1999", "1/4/1999", "1/5/1999"])
    assert frequencies.infer_freq(index) == "B"

