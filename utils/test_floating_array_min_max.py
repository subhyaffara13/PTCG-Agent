
def test_floating_array_min_max(skipna, method, dtype):
    arr = pd.array([0.0, 1.0, None], dtype=dtype)
    func = getattr(arr, method)
    result = func(skipna=skipna)
    if skipna:
        assert result == (0 if method == "min" else 1)
    else:
        assert result is pd.NA

