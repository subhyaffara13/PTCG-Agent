import re

def test_getitem_setitem_datetimeindex():
    N = 50
    # testing with timezone, GH #2785
    rng = date_range("1/1/1990", periods=N, freq="h", tz="US/Eastern", unit="ns")
    ts = Series(np.random.default_rng(2).standard_normal(N), index=rng)

    result = ts["1990-01-01 04:00:00"]
    expected = ts.iloc[4]
    assert result == expected

    result = ts.copy()
    result["1990-01-01 04:00:00"] = 0
    result["1990-01-01 04:00:00"] = ts.iloc[4]
    tm.assert_series_equal(result, ts)

    result = ts["1990-01-01 04:00:00":"1990-01-01 07:00:00"]
    expected = ts[4:8]
    tm.assert_series_equal(result, expected)

    result = ts.copy()
    result["1990-01-01 04:00:00":"1990-01-01 07:00:00"] = 0
    result["1990-01-01 04:00:00":"1990-01-01 07:00:00"] = ts[4:8]
    tm.assert_series_equal(result, ts)

    lb = "1990-01-01 04:00:00"
    rb = "1990-01-01 07:00:00"
    # GH#18435 strings get a pass from tzawareness compat
    result = ts[(ts.index >= lb) & (ts.index <= rb)]
    expected = ts[4:8]
    tm.assert_series_equal(result, expected)

    lb = "1990-01-01 04:00:00-0500"
    rb = "1990-01-01 07:00:00-0500"
    result = ts[(ts.index >= lb) & (ts.index <= rb)]
    expected = ts[4:8]
    tm.assert_series_equal(result, expected)

    # But we do not give datetimes a pass on tzawareness compat
    msg = "Cannot compare tz-naive and tz-aware datetime-like objects"
    naive = datetime(1990, 1, 1, 4)
    for key in [naive, Timestamp(naive), np.datetime64(naive, "ns")]:
        with pytest.raises(KeyError, match=re.escape(repr(key))):
            # GH#36148 as of 2.0 we require tzawareness-compat
            ts[key]

    result = ts.copy()
    # GH#36148 as of 2.0 we do not ignore tzawareness mismatch in indexing,
    #  so setting it as a new key casts to object rather than matching
    #  rng[4]
    result[naive] = ts.iloc[4]
    assert result.index.dtype == object
    tm.assert_index_equal(result.index[:-1], rng.astype(object))
    assert result.index[-1] == naive

    msg = "Cannot compare tz-naive and tz-aware datetime-like objects"
    with pytest.raises(TypeError, match=msg):
        # GH#36148 require tzawareness compat as of 2.0
        ts[naive : datetime(1990, 1, 1, 7)]

    result = ts.copy()
    with pytest.raises(TypeError, match=msg):
        # GH#36148 require tzawareness compat as of 2.0
        result[naive : datetime(1990, 1, 1, 7)] = 0
    with pytest.raises(TypeError, match=msg):
        # GH#36148 require tzawareness compat as of 2.0
        result[naive : datetime(1990, 1, 1, 7)] = 99
    # the __setitems__ here failed, so result should still match ts
    tm.assert_series_equal(result, ts)

    lb = naive
    rb = datetime(1990, 1, 1, 7)
    msg = r"Invalid comparison between dtype=datetime64\[ns, US/Eastern\] and datetime"
    with pytest.raises(TypeError, match=msg):
        # tznaive vs tzaware comparison is invalid
        # see GH#18376, GH#18162
        ts[(ts.index >= lb) & (ts.index <= rb)]

    lb = Timestamp(naive).tz_localize(rng.tzinfo)
    rb = Timestamp(datetime(1990, 1, 1, 7)).tz_localize(rng.tzinfo)
    result = ts[(ts.index >= lb) & (ts.index <= rb)]
    expected = ts[4:8]
    tm.assert_series_equal(result, expected)

    result = ts[ts.index[4]]
    expected = ts.iloc[4]
    assert result == expected

    result = ts[ts.index[4:8]]
    expected = ts[4:8]
    tm.assert_series_equal(result, expected)

    result = ts.copy()
    result[ts.index[4:8]] = 0
    result.iloc[4:8] = ts.iloc[4:8]
    tm.assert_series_equal(result, ts)

    # also test partial date slicing
    result = ts["1990-01-02"]
    expected = ts[24:48]
    tm.assert_series_equal(result, expected)

    result = ts.copy()
    result["1990-01-02"] = 0
    result["1990-01-02"] = ts[24:48]
    tm.assert_series_equal(result, ts)

