
def test_overwrite_node(temp_hdfstore):
    temp_hdfstore["a"] = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )
    ts = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )
    temp_hdfstore["a"] = ts

    tm.assert_series_equal(temp_hdfstore["a"], ts)

