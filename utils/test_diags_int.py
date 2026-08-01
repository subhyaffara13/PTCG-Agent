
def test_diags_int(func):
    d = [[3], [1, 2], [4]]
    offsets = [-1, 0, 1]
    # Until the deprecation period is over, `dtype=None` must be given
    # explicitly to avoid the warning and the cast to an inexact type
    # in diags_array() (gh-23102).
    arr = func(d, offsets=offsets, dtype=None)
    expected = np.array([[1, 4], [3, 2]])
    assert_array_equal(arr.toarray(), expected, strict=True)

