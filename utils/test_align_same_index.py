
def test_align_same_index(datetime_series):
    a, b = datetime_series.align(datetime_series)
    assert a.index is not datetime_series.index
    assert b.index is not datetime_series.index
    assert a.index.is_(datetime_series.index)
    assert b.index.is_(datetime_series.index)

