import copy

def test_from_sequence_no_mutate(copy, cls, dtype):
    nan_arr = np.array(["a", np.nan], dtype=object)
    expected_input = nan_arr.copy()
    na_arr = np.array(["a", pd.NA], dtype=object)

    result = cls._from_sequence(nan_arr, dtype=dtype, copy=copy)

    if cls is ArrowStringArray:
        import pyarrow as pa

        expected = cls(
            pa.array(na_arr, type=pa.string(), from_pandas=True), dtype=dtype
        )
    elif dtype.na_value is np.nan:
        expected = cls(nan_arr, dtype=dtype)
    else:
        expected = cls(na_arr, dtype=dtype)

    tm.assert_extension_array_equal(result, expected)
    tm.assert_numpy_array_equal(nan_arr, expected_input)

