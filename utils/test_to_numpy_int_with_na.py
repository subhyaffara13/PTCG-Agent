
def test_to_numpy_int_with_na(using_nan_is_na):
    # GH51227: ensure to_numpy does not convert int to float
    data = [1, None]
    arr = pd.array(data, dtype="int64[pyarrow]")
    result = arr.to_numpy()
    if not using_nan_is_na:
        expected = np.array([1, pd.NA], dtype=object)
    else:
        expected = np.array([1, np.nan])
        assert isinstance(result[0], float)
    tm.assert_numpy_array_equal(result, expected)

