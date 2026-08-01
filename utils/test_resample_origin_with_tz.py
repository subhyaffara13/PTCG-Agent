
def test_resample_origin_with_tz(unit):
    # GH 31809
    msg = "The origin must have the same timezone as the index."

    tz = "Europe/Paris"
    rng = date_range(
        "2000-01-01 00:00:00", "2000-01-01 02:00", freq="s", tz=tz
    ).as_unit(unit)
    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), index=rng)

    exp_rng = date_range(
        "1999-12-31 23:57:00", "2000-01-01 01:57", freq="5min", tz=tz
    ).as_unit(unit)
    resampled = ts.resample("5min", origin="1999-12-31 23:57:00+00:00").mean()
    tm.assert_index_equal(resampled.index, exp_rng)

    # origin of '1999-31-12 12:02:00+03:00' should be equivalent for this case
    resampled = ts.resample("5min", origin="1999-12-31 12:02:00+03:00").mean()
    tm.assert_index_equal(resampled.index, exp_rng)

    resampled = ts.resample("5min", origin="epoch", offset="2m").mean()
    tm.assert_index_equal(resampled.index, exp_rng)

    with pytest.raises(ValueError, match=msg):
        ts.resample("5min", origin="12/31/1999 23:57:00").mean()

    # if the series is not tz aware, origin should not be tz aware
    rng = date_range("2000-01-01 00:00:00", "2000-01-01 02:00", freq="s").as_unit(unit)
    ts = Series(np.random.default_rng(2).standard_normal(len(rng)), index=rng)
    with pytest.raises(ValueError, match=msg):
        ts.resample("5min", origin="12/31/1999 23:57:00+03:00").mean()

