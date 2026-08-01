
def test_setting_fill_value_fillna_still_works():
    # This is why letting users update fill_value / dtype is bad
    # astype has the same problem.
    arr = SparseArray([1.0, np.nan, 1.0], fill_value=0.0)
    arr.fill_value = np.nan
    result = arr.isna()
    # Can't do direct comparison, since the sp_index will be different
    # So let's convert to ndarray and check there.
    result = np.asarray(result)

    expected = np.array([False, True, False])
    tm.assert_numpy_array_equal(result, expected)

