
def test_chained_where_mask(func):
    df = DataFrame({"a": [1, 4, 2], "b": 1})
    df_orig = df.copy()
    with tm.raises_chained_assignment_error():
        getattr(df["a"], func)(df["a"] > 2, 5, inplace=True)
    tm.assert_frame_equal(df, df_orig)

    with tm.raises_chained_assignment_error():
        getattr(df[["a"]], func)(df["a"] > 2, 5, inplace=True)
    tm.assert_frame_equal(df, df_orig)

