
def test_infer_freq_tz(tz_naive_fixture, expected, dates, unit):
    # see gh-7310, GH#55609
    tz = tz_naive_fixture
    idx = DatetimeIndex(dates, tz=tz).as_unit(unit)
    assert idx.inferred_freq == expected

