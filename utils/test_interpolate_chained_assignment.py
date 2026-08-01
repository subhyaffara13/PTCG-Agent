
def test_interpolate_chained_assignment(func):
    df = DataFrame({"a": [1, np.nan, 2], "b": 1})
    df_orig = df.copy()
    with tm.raises_chained_assignment_error():
        getattr(df["a"], func)(inplace=True)
    tm.assert_frame_equal(df, df_orig)

    with tm.raises_chained_assignment_error():
        getattr(df[["a"]], func)(inplace=True)
    tm.assert_frame_equal(df, df_orig)

