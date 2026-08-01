
def test_resample_offset(unit):
    # GH 31809

    rng = date_range("1/1/2000 00:00:00", "1/1/2000 02:00", freq="s").as_unit(unit)
    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), index=rng)

    resampled = ts.resample("5min", offset="2min").mean()
    exp_rng = date_range("12/31/1999 23:57:00", "1/1/2000 01:57", freq="5min").as_unit(
        unit
    )
    tm.assert_index_equal(resampled.index, exp_rng)

