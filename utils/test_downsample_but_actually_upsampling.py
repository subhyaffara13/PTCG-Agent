
def test_downsample_but_actually_upsampling():
    # this is reindex / asfreq
    rng = date_range("1/1/2012", periods=100, freq="s")
    ts = Series(np.arange(len(rng), dtype="int64"), index=rng)
    result = ts.resample("20s").asfreq()
    expected = Series(
        [0, 20, 40, 60, 80],
        index=date_range("2012-01-01 00:00:00", freq="20s", periods=5),
    )
    tm.assert_series_equal(result, expected)

