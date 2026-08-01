
def test_to_numpy_returns_pdna_default(dtype):
    arr = pd.array(["a", pd.NA, "b"], dtype=dtype)
    result = np.array(arr)
    expected = np.array(["a", dtype.na_value, "b"], dtype=object)
    tm.assert_numpy_array_equal(result, expected)

