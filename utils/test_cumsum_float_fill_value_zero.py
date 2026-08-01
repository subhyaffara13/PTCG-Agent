
def test_cumsum_float_fill_value_zero():
    # GH 62669
    arr = pd.arrays.SparseArray([1.0, 0.0, np.nan, 3.0], fill_value=0.0)
    result = arr.cumsum()
    expected = SparseArray([1.0, 1.0, None, 4.0], fill_value=np.nan)
    tm.assert_sp_array_equal(result, expected)

