
def test_non_datetime_index():
    dates = to_datetime(["1/1/2000", "1/2/2000", "1/3/2000"])
    assert frequencies.infer_freq(dates) == "D"

