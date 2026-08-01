
def test_setslice(datetime_series):
    sl = datetime_series[5:20]
    assert len(sl) == len(sl.index)
    assert sl.index.is_unique is True

