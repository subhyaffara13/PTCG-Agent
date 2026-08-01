
def test_flat_assignment_distinct_allocators():
    a, b, a_obj, b_obj = _make_distinct_arena_arrays(20)
    b.flat = a
    b_obj.flat = a_obj
    assert_array_equal(b, b_obj)

    # fewer values than elements exercises value cycling
    c, _, c_obj, _ = _make_distinct_arena_arrays(20, prefix_a="C")
    c.flat = a[:3]
    c_obj.flat = a_obj[:3]
    assert_array_equal(c, c_obj)

    # short (inline) values into an arena-string destination
    d, _, d_obj, _ = _make_distinct_arena_arrays(20, prefix_a="D")
    d.flat = ["xy"]
    d_obj.flat = ["xy"]
    assert_array_equal(d, d_obj)

