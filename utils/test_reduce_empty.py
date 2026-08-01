
def test_reduce_empty(skipna, dtype, min_count):
    arr = pd.Series([], dtype=dtype)
    result = arr.sum(skipna=skipna, min_count=min_count)
    if min_count == 0:
        assert result == ""
    else:
        assert pd.isna(result)

    # all-missing
    arr = pd.Series([None, None], dtype=dtype)
    result = arr.sum(skipna=skipna, min_count=min_count)
    if skipna and min_count == 0:
        assert result == ""
    else:
        assert pd.isna(result)

