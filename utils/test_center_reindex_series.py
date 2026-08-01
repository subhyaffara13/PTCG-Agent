
def test_center_reindex_series(raw, series):
    # shifter index
    s = [f"x{x:d}" for x in range(12)]
    minp = 10

    series_xp = (
        series.reindex(list(series.index) + s)
        .rolling(window=25, min_periods=minp)
        .apply(f, raw=raw)
        .shift(-12)
        .reindex(series.index)
    )
    series_rs = series.rolling(window=25, min_periods=minp, center=True).apply(
        f, raw=raw
    )
    tm.assert_series_equal(series_xp, series_rs)


def test_center_reindex_series(series, roll_func, kwargs, minp, fill_value):
    # shifter index
    s = [f"x{x:d}" for x in range(12)]

    series_xp = (
        getattr(
            series.reindex(list(series.index) + s).rolling(window=25, min_periods=minp),
            roll_func,
        )(**kwargs)
        .shift(-12)
        .reindex(series.index)
    )
    series_rs = getattr(
        series.rolling(window=25, min_periods=minp, center=True), roll_func
    )(**kwargs)
    if fill_value is not None:
        series_xp = series_xp.fillna(fill_value)
    tm.assert_series_equal(series_xp, series_rs)


def test_center_reindex_series(series, q):
    # shifter index
    s = [f"x{x:d}" for x in range(12)]

    series_xp = (
        series.reindex(list(series.index) + s)
        .rolling(window=25)
        .quantile(q)
        .shift(-12)
        .reindex(series.index)
    )

    series_rs = series.rolling(window=25, center=True).quantile(q)
    tm.assert_series_equal(series_xp, series_rs)


def test_center_reindex_series(series, roll_func):
    # shifter index
    s = [f"x{x:d}" for x in range(12)]

    series_xp = (
        getattr(
            series.reindex(list(series.index) + s).rolling(window=25),
            roll_func,
        )()
        .shift(-12)
        .reindex(series.index)
    )
    series_rs = getattr(series.rolling(window=25, center=True), roll_func)()
    tm.assert_series_equal(series_xp, series_rs)

