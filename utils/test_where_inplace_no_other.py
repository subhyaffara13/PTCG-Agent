
def test_where_inplace_no_other():
    # GH#51685
    df = DataFrame({"a": [1.0, 2.0], "b": ["x", "y"]})
    cond = DataFrame({"a": [True, False], "b": [False, True]})
    result = df.where(cond, inplace=True)
    assert result is df
    expected = DataFrame({"a": [1, np.nan], "b": [np.nan, "y"]})
    tm.assert_frame_equal(df, expected)

