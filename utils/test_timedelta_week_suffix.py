
def test_timedelta_week_suffix():
    # GH#12691 ensure 'W' suffix works as a string passed to Timedelta
    expected = Timedelta("7 days")
    result = Timedelta(1, unit="W")
    assert result == expected

    result = Timedelta("1W")
    assert result == expected

