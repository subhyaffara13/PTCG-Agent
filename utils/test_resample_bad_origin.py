
def test_resample_bad_origin(origin, unit):
    rng = date_range("2000-01-01 00:00:00", "2000-01-01 02:00", freq="s").as_unit(unit)
    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), index=rng)
    msg = (
        "'origin' should be equal to 'epoch', 'start', 'start_day', "
        "'end', 'end_day' or should be a Timestamp convertible type. Got "
        f"'{origin}' instead."
    )
    with pytest.raises(ValueError, match=msg):
        ts.resample("5min", origin=origin)

