
def test_setting_fill_value_updates():
    arr = SparseArray([0.0, np.nan], fill_value=0)
    arr.fill_value = np.nan
    # use private constructor to get the index right
    # otherwise both nans would be un-stored.
    expected = SparseArray._simple_new(
        sparse_array=np.array([np.nan]),
        sparse_index=IntIndex(2, [1]),
        dtype=SparseDtype(float, np.nan),
    )
    tm.assert_sp_array_equal(arr, expected)

