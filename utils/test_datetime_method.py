
def test_datetime_method(method):
    s = pd.Series(pd.date_range("2000", periods=4))
    s.attrs = {"a": 1}
    result = method(s.dt)
    assert result.attrs == {"a": 1}

