
def test_update_chained_assignment():
    df = DataFrame({"a": [1, 2, 3]})
    ser2 = Series([100.0], index=[1])
    df_orig = df.copy()
    with tm.raises_chained_assignment_error():
        df["a"].update(ser2)
    tm.assert_frame_equal(df, df_orig)

    with tm.raises_chained_assignment_error():
        df[["a"]].update(ser2.to_frame())
    tm.assert_frame_equal(df, df_orig)

