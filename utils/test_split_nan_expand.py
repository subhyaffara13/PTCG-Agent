
def test_split_nan_expand(any_string_dtype):
    # gh-18450
    s = Series(["foo,bar,baz", np.nan], dtype=any_string_dtype)
    result = s.str.split(",", expand=True)
    exp = DataFrame(
        [["foo", "bar", "baz"], [np.nan, np.nan, np.nan]], dtype=any_string_dtype
    )
    tm.assert_frame_equal(result, exp)

    # check that these are actually np.nan/pd.NA and not None
    # TODO see GH 18463
    # tm.assert_frame_equal does not differentiate
    if is_object_or_nan_string_dtype(any_string_dtype):
        assert all(np.isnan(x) for x in result.iloc[1])
    else:
        assert all(x is pd.NA for x in result.iloc[1])

