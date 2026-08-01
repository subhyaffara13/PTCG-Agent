
def test_ffill_not_in_axis(func, key, val):
    # GH 21521
    df = DataFrame([[np.nan]])
    result = getattr(df.groupby(**{key: val}), func)()
    expected = df

    tm.assert_frame_equal(result, expected)

