
def test_resample_origin(kwargs, unit):
    # GH 31809
    rng = date_range("2000-01-01 00:00:00", "2000-01-01 02:00", freq="s").as_unit(unit)
    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), index=rng)

    exp_rng = date_range(
        "1999-12-31 23:57:00", "2000-01-01 01:57", freq="5min"
    ).as_unit(unit)

    resampled = ts.resample("5min", **kwargs).mean()
    tm.assert_index_equal(resampled.index, exp_rng)

