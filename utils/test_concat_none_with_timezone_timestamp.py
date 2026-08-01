
def test_concat_none_with_timezone_timestamp():
    # GH#52093
    df1 = DataFrame([{"A": None}])
    df2 = DataFrame([{"A": pd.Timestamp("1990-12-20 00:00:00+00:00")}])
    result = concat([df1, df2], ignore_index=True)
    expected = DataFrame(
        {"A": [None, pd.Timestamp("1990-12-20 00:00:00+00:00")]}, dtype=object
    )
    tm.assert_frame_equal(result, expected)

