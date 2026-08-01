
def test_series_apply_no_suffix_index(by_row):
    # GH36189
    s = Series([4] * 3)
    result = s.apply(["sum", lambda x: x.sum(), lambda x: x.sum()], by_row=by_row)
    expected = Series([12, 12, 12], index=["sum", "<lambda>", "<lambda>"])

    tm.assert_series_equal(result, expected)

