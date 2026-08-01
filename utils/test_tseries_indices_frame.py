
def test_tseries_indices_frame(temp_hdfstore):
    idx = date_range("2020-01-01", periods=10)
    df = DataFrame(np.random.default_rng(2).standard_normal((len(idx), 3)), index=idx)
    temp_hdfstore["a"] = df
    result = temp_hdfstore["a"]

    tm.assert_frame_equal(result, df)
    assert result.index.freq == df.index.freq
    tm.assert_class_equal(result.index, df.index, obj="dataframe index")

    idx = period_range("2020-01-01", periods=10, freq="D")
    df = DataFrame(np.random.default_rng(2).standard_normal((len(idx), 3)), idx)
    temp_hdfstore["a"] = df
    result = temp_hdfstore["a"]

    tm.assert_frame_equal(result, df)
    assert result.index.freq == df.index.freq
    tm.assert_class_equal(result.index, df.index, obj="dataframe index")

