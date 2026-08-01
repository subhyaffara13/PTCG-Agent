
def test_monthly_resample_error(unit):
    # #1451
    dates = date_range("4/16/2012 20:00", periods=5000, freq="h").as_unit(unit)
    ts = Series(np.random.default_rng(2).standard_normal(len(dates)), index=dates)
    # it works!
    ts.resample("ME")

