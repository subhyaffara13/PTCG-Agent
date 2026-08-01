
def test_date_like_qcut_bins(arg, expected_bins, unit):
    # see gh-19891
    arg = arg.as_unit(unit)
    expected_bins = expected_bins.as_unit(unit)
    ser = Series(arg)
    result, result_bins = qcut(ser, 2, retbins=True)
    tm.assert_index_equal(result_bins, expected_bins)

