
def test_to_numpy_without_dtype():
    # GH 54808
    arr = pd.array([True, pd.NA], dtype="boolean[pyarrow]")
    result = arr.to_numpy(na_value=False)
    expected = np.array([True, False], dtype=np.bool_)
    tm.assert_numpy_array_equal(result, expected)

    arr = pd.array([1.0, pd.NA], dtype="float32[pyarrow]")
    result = arr.to_numpy(na_value=0.0)
    expected = np.array([1.0, 0.0], dtype=np.float32)
    tm.assert_numpy_array_equal(result, expected)

