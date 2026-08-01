
def test_iterrows():
    df = DataFrame({"a": 0, "b": 1}, index=[1, 2, 3])
    df_orig = df.copy()

    for _, sub in df.iterrows():
        sub.iloc[0] = 100
    tm.assert_frame_equal(df, df_orig)

