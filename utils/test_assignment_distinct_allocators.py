
def test_assignment_distinct_allocators():
    a, b, a_obj, b_obj = _make_distinct_arena_arrays(40)
    mask = np.arange(40) % 4 == 0

    a[mask] = b[mask]
    a_obj[mask] = b_obj[mask]
    assert_array_equal(a, a_obj)

    idx = np.array([1, 2, 3])
    a[idx] = b[:3]
    a_obj[idx] = b_obj[:3]
    assert_array_equal(a, a_obj)

    np.copyto(a, b, where=~mask)
    np.copyto(a_obj, b_obj, where=~mask)
    assert_array_equal(a, a_obj)

    res = np.select([mask, ~mask], [a, b], default="d" * 20)
    expected = np.select([mask, ~mask], [a_obj, b_obj], default="d" * 20)
    assert_array_equal(res, expected)

