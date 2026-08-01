
def test_nans():
    assert_equal(sc.owens_t(20, np.nan), np.nan)
    assert_equal(sc.owens_t(np.nan, 20), np.nan)
    assert_equal(sc.owens_t(np.nan, np.nan), np.nan)


def test_nans(raw):
    obj = Series(np.random.default_rng(2).standard_normal(50))
    obj[:10] = np.nan
    obj[-10:] = np.nan

    result = obj.rolling(50, min_periods=30).apply(f, raw=raw)
    tm.assert_almost_equal(result.iloc[-1], np.mean(obj[10:-10]))

    # min_periods is working correctly
    result = obj.rolling(20, min_periods=15).apply(f, raw=raw)
    assert isna(result.iloc[23])
    assert not isna(result.iloc[24])

    assert not isna(result.iloc[-6])
    assert isna(result.iloc[-5])

    obj2 = Series(np.random.default_rng(2).standard_normal(20))
    result = obj2.rolling(10, min_periods=5).apply(f, raw=raw)
    assert isna(result.iloc[3])
    assert notna(result.iloc[4])

    result0 = obj.rolling(20, min_periods=0).apply(f, raw=raw)
    result1 = obj.rolling(20, min_periods=1).apply(f, raw=raw)
    tm.assert_almost_equal(result0, result1)


def test_nans(compare_func, roll_func, kwargs):
    obj = Series(np.random.default_rng(2).standard_normal(50))
    obj[:10] = np.nan
    obj[-10:] = np.nan

    result = getattr(obj.rolling(50, min_periods=30), roll_func)(**kwargs)
    tm.assert_almost_equal(result.iloc[-1], compare_func(obj[10:-10]))

    # min_periods is working correctly
    result = getattr(obj.rolling(20, min_periods=15), roll_func)(**kwargs)
    assert isna(result.iloc[23])
    assert not isna(result.iloc[24])

    assert not isna(result.iloc[-6])
    assert isna(result.iloc[-5])

    obj2 = Series(np.random.default_rng(2).standard_normal(20))
    result = getattr(obj2.rolling(10, min_periods=5), roll_func)(**kwargs)
    assert isna(result.iloc[3])
    assert notna(result.iloc[4])

    if roll_func != "sum":
        result0 = getattr(obj.rolling(20, min_periods=0), roll_func)(**kwargs)
        result1 = getattr(obj.rolling(20, min_periods=1), roll_func)(**kwargs)
        tm.assert_almost_equal(result0, result1)


def test_nans(q):
    compare_func = partial(scoreatpercentile, per=q)
    obj = Series(np.random.default_rng(2).standard_normal(50))
    obj[:10] = np.nan
    obj[-10:] = np.nan

    result = obj.rolling(50, min_periods=30).quantile(q)
    tm.assert_almost_equal(result.iloc[-1], compare_func(obj[10:-10]))

    # min_periods is working correctly
    result = obj.rolling(20, min_periods=15).quantile(q)
    assert isna(result.iloc[23])
    assert not isna(result.iloc[24])

    assert not isna(result.iloc[-6])
    assert isna(result.iloc[-5])

    obj2 = Series(np.random.default_rng(2).standard_normal(20))
    result = obj2.rolling(10, min_periods=5).quantile(q)
    assert isna(result.iloc[3])
    assert notna(result.iloc[4])

    result0 = obj.rolling(20, min_periods=0).quantile(q)
    result1 = obj.rolling(20, min_periods=1).quantile(q)
    tm.assert_almost_equal(result0, result1)


def test_nans(sp_func, roll_func):
    sp_stats = pytest.importorskip("scipy.stats")

    compare_func = partial(getattr(sp_stats, sp_func), bias=False)
    obj = Series(np.random.default_rng(2).standard_normal(50))
    obj[:10] = np.nan
    obj[-10:] = np.nan

    result = getattr(obj.rolling(50, min_periods=30), roll_func)()
    tm.assert_almost_equal(result.iloc[-1], compare_func(obj[10:-10]))

    # min_periods is working correctly
    result = getattr(obj.rolling(20, min_periods=15), roll_func)()
    assert isna(result.iloc[23])
    assert not isna(result.iloc[24])

    assert not isna(result.iloc[-6])
    assert isna(result.iloc[-5])

    obj2 = Series(np.random.default_rng(2).standard_normal(20))
    result = getattr(obj2.rolling(10, min_periods=5), roll_func)()
    assert isna(result.iloc[3])
    assert notna(result.iloc[4])

    result0 = getattr(obj.rolling(20, min_periods=0), roll_func)()
    result1 = getattr(obj.rolling(20, min_periods=1), roll_func)()
    tm.assert_almost_equal(result0, result1)

