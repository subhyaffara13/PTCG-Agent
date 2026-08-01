
def test_filter_and_transform_with_multiple_non_unique_int_index():
    # GH4620
    index = [1, 1, 1, 2, 0, 0, 0, 1]
    df = DataFrame(
        {"pid": [1, 1, 1, 2, 2, 3, 3, 3], "tag": [23, 45, 62, 24, 45, 34, 25, 62]},
        index=index,
    )
    grouped_df = df.groupby("tag")
    ser = df["pid"]
    grouped_ser = ser.groupby(df["tag"])
    expected_indexes = [1, 2, 4, 7]

    # Filter DataFrame
    actual = grouped_df.filter(lambda x: len(x) > 1)
    expected = df.iloc[expected_indexes]
    tm.assert_frame_equal(actual, expected)

    actual = grouped_df.filter(lambda x: len(x) > 1, dropna=False)
    # Cast to avoid upcast when setting nan below
    expected = df.copy().astype("float64")
    expected.iloc[[0, 3, 5, 6]] = np.nan
    tm.assert_frame_equal(actual, expected)

    # Filter Series
    actual = grouped_ser.filter(lambda x: len(x) > 1)
    expected = ser.take(expected_indexes)
    tm.assert_series_equal(actual, expected)

    actual = grouped_ser.filter(lambda x: len(x) > 1, dropna=False)
    expected = Series([np.nan, 1, 1, np.nan, 2, np.nan, np.nan, 3], index, name="pid")
    # ^ made manually because this can get confusing!
    tm.assert_series_equal(actual, expected)

    # Transform Series
    actual = grouped_ser.transform(len)
    expected = Series([1, 2, 2, 1, 2, 1, 1, 2], index, name="pid")
    tm.assert_series_equal(actual, expected)

    # Transform (a column from) DataFrameGroupBy
    actual = grouped_df.pid.transform(len)
    tm.assert_series_equal(actual, expected)

