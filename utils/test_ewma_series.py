
def test_ewma_series(series, name):
    series_result = getattr(series.ewm(com=10), name)()
    assert isinstance(series_result, Series)

