
def test_drop_errors_ignore(labels, level):
    # GH 8594
    mi = MultiIndex.from_arrays([[1, 2, 3], [4, 5, 6]], names=["a", "b"])
    s = Series([10, 20, 30], index=mi)
    df = DataFrame([10, 20, 30], index=mi)

    expected_s = s.drop(labels, level=level, errors="ignore")
    tm.assert_series_equal(s, expected_s)

    expected_df = df.drop(labels, level=level, errors="ignore")
    tm.assert_frame_equal(df, expected_df)

