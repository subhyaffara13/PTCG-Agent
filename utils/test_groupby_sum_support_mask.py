
def test_groupby_sum_support_mask(any_numeric_ea_dtype, func, val):
    # GH#37493
    df = DataFrame({"a": 1, "b": [1, 2, pd.NA]}, dtype=any_numeric_ea_dtype)
    result = getattr(df.groupby("a"), func)()
    expected = DataFrame(
        {"b": [val]},
        index=Index([1], name="a", dtype=any_numeric_ea_dtype),
        dtype=any_numeric_ea_dtype,
    )
    tm.assert_frame_equal(result, expected)

