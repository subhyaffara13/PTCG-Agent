
def test_concatenate_distinct_allocators():
    a, b, a_obj, b_obj = _make_distinct_arena_arrays(50)
    expected = np.concatenate([a_obj, b_obj])
    assert_array_equal(np.concatenate([a, b]), expected)
    assert_array_equal(np.concatenate([a, b], axis=None), expected)

    out = np.empty(100, dtype="T")
    np.concatenate([a, b], out=out)
    assert_array_equal(out, expected)

    assert_array_equal(np.stack([a, b]), np.stack([a_obj, b_obj]))
    assert_array_equal(np.vstack([a, b]), np.vstack([a_obj, b_obj]))
    assert_array_equal(np.hstack([a, b]), expected)

