
def test_not_change_nan_loc(series, new_series, expected_ser):
    # GH 28403
    df = DataFrame({"A": series})
    df.loc[:, "A"] = new_series
    expected = DataFrame({"A": expected_ser})
    tm.assert_frame_equal(df.isna(), expected)
    tm.assert_frame_equal(df.notna(), ~expected)

