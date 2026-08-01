
def test_mask_inplace_no_other():
    # GH#51685
    df = DataFrame({"a": [1.0, 2.0], "b": ["x", "y"]})
    cond = DataFrame({"a": [True, False], "b": [False, True]})
    df.mask(cond, inplace=True)
    expected = DataFrame({"a": [np.nan, 2], "b": ["x", np.nan]})
    tm.assert_frame_equal(df, expected)

