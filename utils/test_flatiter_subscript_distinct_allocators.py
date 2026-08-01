
def test_flatiter_subscript_distinct_allocators():
    a, _, a_obj, _ = _make_distinct_arena_arrays(20)

    assert_array_equal(np.array(a.flat[:1]), a_obj[:1])

    for index in [
        slice(None, 1), slice(1, None), slice(None, None, 3),
        np.array([3, 0, 17]),
        np.arange(20) % 3 == 0,
    ]:
        res = a.flat[index]
        expected = a_obj[index]
        assert_array_equal(res, expected)
        # element reads resolve through res's own descriptor
        for i in range(len(expected)):
            assert res[i] == expected[i]

    assert a.flat[3] == a_obj[3]
    assert_array_equal(np.array(a.flat), a_obj)
    assert_array_equal(a.flat.copy(), a_obj)

