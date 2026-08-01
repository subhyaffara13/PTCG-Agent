
def test_indexing_ops_distinct_allocators():
    a, b, a_obj, b_obj = _make_distinct_arena_arrays(60)
    idx = np.array([5, 3, 50, 7] * 3)

    out = np.empty(len(idx), dtype="T")
    np.take(a, idx, out=out)
    assert_array_equal(out, a_obj[idx])

    assert_array_equal(np.tile(a[:5], 3), np.tile(a_obj[:5], 3))
    assert_array_equal(np.roll(a, 7), np.roll(a_obj, 7))
    assert_array_equal(np.repeat(a[:10], 3), np.repeat(a_obj[:10], 3))
    assert_array_equal(np.delete(a, idx[:4]), np.delete(a_obj, idx[:4]))
    assert_array_equal(
        np.insert(a, 3, b[:4]), np.insert(a_obj, 3, b_obj[:4])
    )
    assert_array_equal(np.append(a, b), np.append(a_obj, b_obj))

