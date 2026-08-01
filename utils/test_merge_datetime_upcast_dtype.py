
def test_merge_datetime_upcast_dtype():
    # https://github.com/pandas-dev/pandas/issues/31208
    df1 = DataFrame({"x": ["a", "b", "c"], "y": ["1", "2", "4"]})
    df2 = DataFrame(
        {"y": ["1", "2", "3"], "z": pd.to_datetime(["2000", "2001", "2002"])}
    )
    result = merge(df1, df2, how="left", on="y")
    expected = DataFrame(
        {
            "x": ["a", "b", "c"],
            "y": ["1", "2", "4"],
            "z": pd.to_datetime(["2000", "2001", "NaT"]),
        }
    )
    tm.assert_frame_equal(result, expected)

