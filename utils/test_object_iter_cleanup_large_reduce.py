
def test_object_iter_cleanup_large_reduce(arr):
    # More complicated calls are possible for large arrays:
    out = np.ones(8000, dtype=np.intp)
    # force casting with `dtype=object`
    res = np.sum(arr, axis=(1, 2), dtype=object, out=out)
    assert_array_equal(res, np.full(8000, 4, dtype=object))

