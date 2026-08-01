
def test_walk(where, expected, temp_hdfstore):
    # GH10143
    objs = {
        "df1": DataFrame([1, 2, 3]),
        "df2": DataFrame([4, 5, 6]),
        "df3": DataFrame([6, 7, 8]),
        "df4": DataFrame([9, 10, 11]),
        "s1": Series([10, 9, 8]),
        # Next 3 items aren't pandas objects and should be ignored
        "a1": np.array([[1, 2, 3], [4, 5, 6]]),
        "tb1": np.array([(1, 2, 3), (4, 5, 6)], dtype="i,i,i"),
        "tb2": np.array([(7, 8, 9), (10, 11, 12)], dtype="i,i,i"),
    }

    store = temp_hdfstore
    store.put("/first_group/df1", objs["df1"])
    store.put("/first_group/df2", objs["df2"])
    store.put("/second_group/df3", objs["df3"])
    store.put("/second_group/s1", objs["s1"])
    store.put("/second_group/third_group/df4", objs["df4"])
    # Create non-pandas objects
    store._handle.create_array("/first_group", "a1", objs["a1"])
    store._handle.create_table("/first_group", "tb1", obj=objs["tb1"])
    store._handle.create_table("/second_group", "tb2", obj=objs["tb2"])

    assert len(list(store.walk(where=where))) == len(expected)
    for path, groups, leaves in store.walk(where=where):
        assert path in expected
        expected_groups, expected_frames = expected[path]
        assert expected_groups == set(groups)
        assert expected_frames == set(leaves)
        for leaf in leaves:
            frame_path = "/".join([path, leaf])
            obj = store.get(frame_path)
            if "df" in leaf:
                tm.assert_frame_equal(obj, objs[leaf])
            else:
                tm.assert_series_equal(obj, objs[leaf])

