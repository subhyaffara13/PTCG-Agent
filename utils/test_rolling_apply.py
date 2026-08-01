
def test_rolling_apply(engine_and_raw, step):
    engine, raw = engine_and_raw

    expected = Series([], dtype="float64")
    result = expected.rolling(10, step=step).apply(
        lambda x: x.mean(), engine=engine, raw=raw
    )
    tm.assert_series_equal(result, expected)

    # gh-8080
    s = Series([None, None, None])
    result = s.rolling(2, min_periods=0, step=step).apply(
        lambda x: len(x), engine=engine, raw=raw
    )
    expected = Series([1.0, 2.0, 2.0])[::step]
    tm.assert_series_equal(result, expected)

    result = s.rolling(2, min_periods=0, step=step).apply(len, engine=engine, raw=raw)
    tm.assert_series_equal(result, expected)

