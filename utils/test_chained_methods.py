
def test_chained_methods(method, idx):
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [0.1, 0.2, 0.3]})
    df_orig = df.copy()

    # modify df2 -> don't modify df
    df2 = method(df)
    df2.iloc[0, idx] = 0
    tm.assert_frame_equal(df, df_orig)

    # modify df -> don't modify df2
    df2 = method(df)
    df.iloc[0, 0] = 0
    tm.assert_frame_equal(df2.iloc[:, idx:], df_orig)

