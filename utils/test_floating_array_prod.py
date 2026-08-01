
def test_floating_array_prod(skipna, min_count, dtype):
    arr = pd.array([1.0, 2.0, None], dtype=dtype)
    result = arr.prod(skipna=skipna, min_count=min_count)
    if skipna and min_count == 0:
        assert result == 2
    else:
        assert result is pd.NA

