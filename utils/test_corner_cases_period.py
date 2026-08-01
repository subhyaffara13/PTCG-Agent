
def test_corner_cases_period(simple_period_range_series):
    # miscellaneous test coverage
    len0pts = simple_period_range_series("2007-01", "2010-05", freq="M")[:0]
    # it works
    result = len0pts.resample("Y-DEC").mean()
    assert len(result) == 0

