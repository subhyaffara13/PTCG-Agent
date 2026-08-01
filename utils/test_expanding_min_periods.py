
def test_expanding_min_periods(func, static_comp):
    ser = Series(np.random.default_rng(2).standard_normal(50))

    result = getattr(ser.expanding(min_periods=30), func)()
    assert result[:29].isna().all()
    tm.assert_almost_equal(result.iloc[-1], static_comp(ser[:50]))

    # min_periods is working correctly
    result = getattr(ser.expanding(min_periods=15), func)()
    assert isna(result.iloc[13])
    assert notna(result.iloc[14])

    ser2 = Series(np.random.default_rng(2).standard_normal(20))
    result = getattr(ser2.expanding(min_periods=5), func)()
    assert isna(result[3])
    assert notna(result[4])

    # min_periods=0
    result0 = getattr(ser.expanding(min_periods=0), func)()
    result1 = getattr(ser.expanding(min_periods=1), func)()
    tm.assert_almost_equal(result0, result1)

    result = getattr(ser.expanding(min_periods=1), func)()
    tm.assert_almost_equal(result.iloc[-1], static_comp(ser[:50]))

