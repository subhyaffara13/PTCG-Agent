
def test_multiple_functions_tuples_and_non_tuples(df):
    # #1359
    # Columns B and C would cause partial failure
    df = df.drop(columns=["B", "C"])

    funcs = [("foo", "mean"), "std"]
    ex_funcs = [("foo", "mean"), ("std", "std")]

    result = df.groupby("A")["D"].agg(funcs)
    expected = df.groupby("A")["D"].agg(ex_funcs)
    tm.assert_frame_equal(result, expected)

    result = df.groupby("A").agg(funcs)
    expected = df.groupby("A").agg(ex_funcs)
    tm.assert_frame_equal(result, expected)

