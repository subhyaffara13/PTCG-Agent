
def test_agg_std():
    df = DataFrame(np.arange(6).reshape(3, 2), columns=["A", "B"])

    result = df.agg(np.std, ddof=1)
    expected = Series({"A": 2.0, "B": 2.0}, dtype=float)
    tm.assert_series_equal(result, expected)

    result = df.agg([np.std], ddof=1)
    expected = DataFrame({"A": 2.0, "B": 2.0}, index=["std"])
    tm.assert_frame_equal(result, expected)

