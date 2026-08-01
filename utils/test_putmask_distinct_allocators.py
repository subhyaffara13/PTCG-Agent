
def test_putmask_distinct_allocators():
    a, b, a_obj, b_obj = _make_distinct_arena_arrays(100)
    mask = np.arange(100) % 3 == 0
    np.putmask(a, mask, b)
    np.putmask(a_obj, mask, b_obj)
    assert_array_equal(a, a_obj)

    # fewer values than mask entries exercises value cycling
    np.putmask(a, ~mask, b[:7])
    np.putmask(a_obj, ~mask, b_obj[:7])
    assert_array_equal(a, a_obj)

    # all-short-string destination, so its arena is empty
    c = np.array(["x"] * 100, dtype="T")
    np.putmask(c, mask, b)
    assert_array_equal(c[mask], b_obj[mask])
    assert_array_equal(c[~mask], "x")

    # a non-contiguous destination is written through a writeback copy
    d, _, d_obj, _ = _make_distinct_arena_arrays(100, prefix_a="D")
    np.putmask(d[::2], mask[::2], b[:50])
    np.putmask(d_obj[::2], mask[::2], b_obj[:50])
    assert_array_equal(d, d_obj)

