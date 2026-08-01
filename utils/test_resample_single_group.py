
def test_resample_single_group(end, unit):
    mysum = lambda x: x.sum()

    rng = date_range("2000-1-1", f"2000-{end}-10", freq="D").as_unit(unit)
    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), index=rng)
    tm.assert_series_equal(ts.resample("ME").sum(), ts.resample("ME").apply(mysum))

