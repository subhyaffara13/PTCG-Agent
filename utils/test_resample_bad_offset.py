
def test_resample_bad_offset(offset, unit):
    rng = date_range("2000-01-01 00:00:00", "2000-01-01 02:00", freq="s").as_unit(unit)
    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), index=rng)
    msg = f"'offset' should be a Timedelta convertible type. Got '{offset}' instead."
    with pytest.raises(ValueError, match=msg):
        ts.resample("5min", offset=offset)

