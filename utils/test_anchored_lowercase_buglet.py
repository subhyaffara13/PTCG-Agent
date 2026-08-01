
def test_anchored_lowercase_buglet(unit):
    dates = date_range("4/16/2012 20:00", periods=50000, freq="s").as_unit(unit)
    ts = Series(np.random.default_rng(2).standard_normal(len(dates)), index=dates)
    # it works!
    msg = "'d' is deprecated and will be removed in a future version."
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        ts.resample("d").mean()

