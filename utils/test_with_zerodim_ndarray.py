
def test_with_zerodim_ndarray():
    # GH#27910
    arr = SparseArray([0, 1], fill_value=0)

    result = arr * np.array(2)
    expected = arr * 2
    tm.assert_sp_array_equal(result, expected)

