
def test_clip_chained_inplace():
    df = DataFrame({"a": [1, 4, 2], "b": 1})
    df_orig = df.copy()
    with tm.raises_chained_assignment_error():
        df["a"].clip(1, 2, inplace=True)
    tm.assert_frame_equal(df, df_orig)

    with tm.raises_chained_assignment_error():
        df[["a"]].clip(1, 2, inplace=True)
    tm.assert_frame_equal(df, df_orig)

