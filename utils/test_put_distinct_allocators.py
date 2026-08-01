
def test_put_distinct_allocators(mode):
    a, b, a_obj, b_obj = _make_distinct_arena_arrays(100)
    inds = np.arange(0, 100, 2)
    np.put(a, inds, b[:50], mode=mode)
    np.put(a_obj, inds, b_obj[:50], mode=mode)
    assert_array_equal(a, a_obj)

    # values must cycle when there are fewer of them than indices
    np.put(a, inds, b[:3], mode=mode)
    np.put(a_obj, inds, b_obj[:3], mode=mode)
    assert_array_equal(a, a_obj)

    # all-short-string destination, so its arena is empty
    c = np.array(["x"] * 100, dtype="T")
    np.put(c, inds, b[:50], mode=mode)
    assert_array_equal(c[inds], b_obj[:50])
    assert_array_equal(c[1::2], "x")

    # a non-contiguous destination is written through a writeback copy
    d, _, d_obj, _ = _make_distinct_arena_arrays(100, prefix_a="D")
    np.put(d[::2], np.arange(50), b[:50], mode=mode)
    np.put(d_obj[::2], np.arange(50), b_obj[:50], mode=mode)
    assert_array_equal(d, d_obj)

