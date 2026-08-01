
def test_arrfuncs_zeros(arrfunc, expected):
    arr = np.zeros(10, dtype="T")
    result = arrfunc(arr)
    if expected is None:
        expected = arr
    assert_array_equal(result, expected, strict=True)

