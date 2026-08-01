
def test_groupsort_indexer():
    a = np.random.default_rng(2).integers(0, 1000, 100).astype(np.intp)
    b = np.random.default_rng(2).integers(0, 1000, 100).astype(np.intp)

    result = libalgos.groupsort_indexer(a, 1000)[0]

    # need to use a stable sort
    # np.argsort returns int, groupsort_indexer
    # always returns intp
    expected = np.argsort(a, kind="mergesort")
    expected = expected.astype(np.intp)

    tm.assert_numpy_array_equal(result, expected)

    # compare with lexsort
    # np.lexsort returns int, groupsort_indexer
    # always returns intp
    key = a * 1000 + b
    result = libalgos.groupsort_indexer(key, 1000000)[0]
    expected = np.lexsort((b, a))
    expected = expected.astype(np.intp)

    tm.assert_numpy_array_equal(result, expected)

