
def test_upsample_apply_functions(unit):
    # #1596
    rng = date_range("2012-06-12", periods=4, freq="h").as_unit(unit)

    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), index=rng)

    result = ts.resample("20min").aggregate(["mean", "sum"])
    assert isinstance(result, DataFrame)

