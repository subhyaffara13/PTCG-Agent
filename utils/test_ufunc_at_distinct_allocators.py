
def test_ufunc_at_distinct_allocators():
    a, b, a_obj, b_obj = _make_distinct_arena_arrays(10)
    idx = np.array([0, 3, 3, 7])

    np.maximum.at(a, idx, b[:4])
    np.maximum.at(a_obj, idx, b_obj[:4])
    assert_array_equal(a, a_obj)

    c, d, c_obj, d_obj = _make_distinct_arena_arrays(10, "C", "D")
    np.add.at(c, idx, d[:4])
    np.add.at(c_obj, idx, d_obj[:4])
    assert_array_equal(c, c_obj)

