
def test_fillna_chained_assignment():
    df = DataFrame({"a": [1, np.nan, 2], "b": 1})
    df_orig = df.copy()
    with tm.raises_chained_assignment_error():
        df["a"].fillna(100, inplace=True)
    tm.assert_frame_equal(df, df_orig)

    with tm.raises_chained_assignment_error():
        df[["a"]].fillna(100, inplace=True)
    tm.assert_frame_equal(df, df_orig)

