
def test_timedelta_property(attr):
    s = pd.Series(pd.timedelta_range("2000", periods=4))
    s.attrs = {"a": 1}
    result = getattr(s.dt, attr)
    assert result.attrs == {"a": 1}

