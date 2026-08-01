
def test_integer_array_prod(skipna, min_count, any_int_ea_dtype):
    dtype = any_int_ea_dtype
    arr = pd.array([1, 2, None], dtype=dtype)
    result = arr.prod(skipna=skipna, min_count=min_count)
    if skipna and min_count == 0:
        assert result == 2
    else:
        assert result is pd.NA

