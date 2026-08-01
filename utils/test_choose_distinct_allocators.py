
def test_choose_distinct_allocators(mode):
    n = 100
    idx = np.arange(n) % 2
    # an all-short-string choice mixed with arena-string choices
    c0 = np.array(["x"] * n, dtype="T")
    c1, c2, c1_obj, c2_obj = _make_distinct_arena_arrays(n)
    c0_obj = np.array(["x"] * n, dtype=object)

    expected = np.choose(idx, [c0_obj, c1_obj], mode=mode)
    assert_array_equal(np.choose(idx, [c0, c1], mode=mode), expected)

    expected = np.choose(idx, [c1_obj, c2_obj], mode=mode)
    assert_array_equal(np.choose(idx, [c1, c2], mode=mode), expected)

    # out= with its own independently created instance
    out = np.empty(n, dtype="T")
    np.choose(idx, [c1, c2], mode=mode, out=out)
    assert_array_equal(out, expected)

