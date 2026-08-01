
def test_where_distinct_allocators():
    a, b, a_obj, b_obj = _make_distinct_arena_arrays(101)
    mask = np.arange(101) % 3 == 0
    assert_array_equal(np.where(mask, a, b), np.where(mask, a_obj, b_obj))

