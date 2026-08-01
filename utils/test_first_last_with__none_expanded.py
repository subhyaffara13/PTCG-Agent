
def test_first_last_with_None_expanded(method, df, expected):
    # GH 32800, 38286
    result = getattr(df.groupby("id"), method)()
    tm.assert_frame_equal(result, expected)

