
def test_tseries_indices_series(temp_hdfstore):
    idx = date_range("2020-01-01", periods=10)
    ser = Series(np.random.default_rng(2).standard_normal(len(idx)), idx)
    temp_hdfstore["a"] = ser
    result = temp_hdfstore["a"]

    tm.assert_series_equal(result, ser)
    assert result.index.freq == ser.index.freq
    tm.assert_class_equal(result.index, ser.index, obj="series index")

    idx = period_range("2020-01-01", periods=10, freq="D")
    ser = Series(np.random.default_rng(2).standard_normal(len(idx)), idx)
    temp_hdfstore["a"] = ser
    result = temp_hdfstore["a"]

    tm.assert_series_equal(result, ser)
    assert result.index.freq == ser.index.freq
    tm.assert_class_equal(result.index, ser.index, obj="series index")

