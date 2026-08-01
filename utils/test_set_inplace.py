
def test_set_inplace():
    # https://github.com/pandas-dev/pandas/issues/47449
    # Ensure we don't only update the DataFrame inplace, but also the actual
    # column values, such that references to this column also get updated
    df = DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
    result_view = df[:]
    ser = df["A"]
    df.eval("A = B + C", inplace=True)
    expected = DataFrame({"A": [11, 13, 15], "B": [4, 5, 6], "C": [7, 8, 9]})
    tm.assert_frame_equal(df, expected)
    expected = Series([1, 2, 3], name="A")
    tm.assert_series_equal(ser, expected)
    tm.assert_series_equal(result_view["A"], expected)

