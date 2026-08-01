
def test_reduce_missing(skipna, dtype):
    arr = pd.Series([None, "a", None, "b", "c", None], dtype=dtype)
    result = arr.sum(skipna=skipna)
    if skipna:
        assert result == "abc"
    else:
        assert pd.isna(result)

