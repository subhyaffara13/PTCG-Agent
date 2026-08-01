
def test_agg_np_size():
    # GH#42203, GH#48328
    df = DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=["A", "B", "C"])

    result = df.agg({"A": [np.size]})
    expected = DataFrame({"A": [3]}, index=["size"])
    tm.assert_frame_equal(result, expected)

    result = df.agg({"A": np.size})
    expected = Series({"A": 3})
    tm.assert_series_equal(result, expected)

    result = df.agg({"A": [np.mean, np.size]})
    expected = DataFrame({"A": [4.0, 3.0]}, index=["mean", "size"])
    tm.assert_frame_equal(result, expected)

