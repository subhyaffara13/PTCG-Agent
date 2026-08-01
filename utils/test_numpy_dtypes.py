
def test_numpy_dtypes(source_dtypes, expected_common_dtype):
    source_dtypes = [pandas_dtype(x) for x in source_dtypes]
    assert find_common_type(source_dtypes) == expected_common_dtype

