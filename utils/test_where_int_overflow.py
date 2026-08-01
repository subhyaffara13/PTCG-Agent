
def test_where_int_overflow(replacement):
    # GH 31687
    df = DataFrame([[1.0, 2e25, "nine"], [np.nan, 0.1, None]])
    result = df.where(pd.notnull(df), replacement)
    expected = DataFrame([[1.0, 2e25, "nine"], [replacement, 0.1, replacement]])

    tm.assert_frame_equal(result, expected)

