
def test_min_periods(raw, series, minp, step):
    result = series.rolling(len(series) + 1, min_periods=minp, step=step).apply(
        f, raw=raw
    )
    expected = series.rolling(len(series), min_periods=minp, step=step).apply(
        f, raw=raw
    )
    nan_mask = isna(result)
    tm.assert_series_equal(nan_mask, isna(expected))

    nan_mask = ~nan_mask
    tm.assert_almost_equal(result[nan_mask], expected[nan_mask])


def test_min_periods(series, minp, roll_func, kwargs, step):
    result = getattr(
        series.rolling(len(series) + 1, min_periods=minp, step=step), roll_func
    )(**kwargs)
    expected = getattr(
        series.rolling(len(series), min_periods=minp, step=step), roll_func
    )(**kwargs)
    nan_mask = isna(result)
    tm.assert_series_equal(nan_mask, isna(expected))

    nan_mask = ~nan_mask
    tm.assert_almost_equal(result[nan_mask], expected[nan_mask])


def test_min_periods(series, minp, q, step):
    result = series.rolling(len(series) + 1, min_periods=minp, step=step).quantile(q)
    expected = series.rolling(len(series), min_periods=minp, step=step).quantile(q)
    nan_mask = isna(result)
    tm.assert_series_equal(nan_mask, isna(expected))

    nan_mask = ~nan_mask
    tm.assert_almost_equal(result[nan_mask], expected[nan_mask])


def test_min_periods(series, minp, roll_func, step):
    result = getattr(
        series.rolling(len(series) + 1, min_periods=minp, step=step), roll_func
    )()
    expected = getattr(
        series.rolling(len(series), min_periods=minp, step=step), roll_func
    )()
    nan_mask = isna(result)
    tm.assert_series_equal(nan_mask, isna(expected))

    nan_mask = ~nan_mask
    tm.assert_almost_equal(result[nan_mask], expected[nan_mask])

