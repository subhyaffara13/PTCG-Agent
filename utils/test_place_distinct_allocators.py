
def test_place_distinct_allocators():
    a = np.array(["ab", "cd", "ef"], dtype="T")
    np.place(a, [True, False, True], np.array(["xy", "zw"], dtype="T"))
    assert_array_equal(a, ["xy", "cd", "zw"])

    a, b, a_obj, b_obj = _make_distinct_arena_arrays(100)
    mask = np.arange(100) % 3 == 0
    # fewer values than selected entries exercises value cycling
    np.place(a, mask, b[:7])
    np.place(a_obj, mask, b_obj[:7])
    assert_array_equal(a, a_obj)

    # all-short-string destination, so its arena is empty
    c = np.array(["x"] * 100, dtype="T")
    np.place(c, mask, b)
    assert_array_equal(c[mask], b_obj[: mask.sum()])
    assert_array_equal(c[~mask], "x")

