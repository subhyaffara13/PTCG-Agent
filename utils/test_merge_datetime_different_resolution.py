
def test_merge_datetime_different_resolution(tz, join_type):
    # https://github.com/pandas-dev/pandas/issues/53200
    vals = [
        pd.Timestamp(2023, 5, 12, tz=tz),
        pd.Timestamp(2023, 5, 13, tz=tz),
        pd.Timestamp(2023, 5, 14, tz=tz),
    ]
    df1 = DataFrame({"t": vals[:2], "a": [1.0, 2.0]})
    df1["t"] = df1["t"].dt.as_unit("ns")
    df2 = DataFrame({"t": vals[1:], "b": [1.0, 2.0]})
    df2["t"] = df2["t"].dt.as_unit("s")

    expected = DataFrame({"t": vals, "a": [1.0, 2.0, np.nan], "b": [np.nan, 1.0, 2.0]})
    expected["t"] = expected["t"].dt.as_unit("ns")
    if join_type == "inner":
        expected = expected.iloc[[1]].reset_index(drop=True)
    elif join_type == "left":
        expected = expected.iloc[[0, 1]]
    elif join_type == "right":
        expected = expected.iloc[[1, 2]].reset_index(drop=True)

    result = df1.merge(df2, on="t", how=join_type)
    tm.assert_frame_equal(result, expected)

