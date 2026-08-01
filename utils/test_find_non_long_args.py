
def test_find_non_long_args(dtype):
    element = 'abcd'
    start = dtype(0)
    end = dtype(len(element))
    arr = np.array([element])
    result = np._core.umath.find(arr, "a", start, end)
    assert result.dtype == np.dtype("intp")
    assert result == 0

