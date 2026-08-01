
def test_time_rule_series(raw, series):
    win = 25
    minp = 10
    ser = series[::2].resample("B").mean()
    series_result = ser.rolling(window=win, min_periods=minp).apply(f, raw=raw)
    last_date = series_result.index[-1]
    prev_date = last_date - 24 * offsets.BDay()

    trunc_series = series[::2].truncate(prev_date, last_date)
    tm.assert_almost_equal(series_result.iloc[-1], np.mean(trunc_series))


def test_time_rule_series(series, compare_func, roll_func, kwargs, minp):
    win = 25
    ser = series[::2].resample("B").mean()
    series_result = getattr(ser.rolling(window=win, min_periods=minp), roll_func)(
        **kwargs
    )
    last_date = series_result.index[-1]
    prev_date = last_date - 24 * offsets.BDay()

    trunc_series = series[::2].truncate(prev_date, last_date)
    tm.assert_almost_equal(series_result.iloc[-1], compare_func(trunc_series))


def test_time_rule_series(series, q):
    compare_func = partial(scoreatpercentile, per=q)
    win = 25
    ser = series[::2].resample("B").mean()
    series_result = ser.rolling(window=win, min_periods=10).quantile(q)
    last_date = series_result.index[-1]
    prev_date = last_date - 24 * offsets.BDay()

    trunc_series = series[::2].truncate(prev_date, last_date)
    tm.assert_almost_equal(series_result.iloc[-1], compare_func(trunc_series))


def test_time_rule_series(series, sp_func, roll_func):
    sp_stats = pytest.importorskip("scipy.stats")

    compare_func = partial(getattr(sp_stats, sp_func), bias=False)
    win = 25
    ser = series[::2].resample("B").mean()
    series_result = getattr(ser.rolling(window=win, min_periods=10), roll_func)()
    last_date = series_result.index[-1]
    prev_date = last_date - 24 * offsets.BDay()

    trunc_series = series[::2].truncate(prev_date, last_date)
    tm.assert_almost_equal(series_result.iloc[-1], compare_func(trunc_series))

