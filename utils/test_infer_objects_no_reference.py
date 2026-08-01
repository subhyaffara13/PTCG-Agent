
def test_infer_objects_no_reference(using_infer_string):
    df = DataFrame(
        {
            "a": [1, 2],
            "b": Series(["x", "y"], dtype=object),
            "c": 1,
            "d": Series(
                [Timestamp("2019-12-31"), Timestamp("2020-12-31")], dtype="object"
            ),
            "e": Series(["z", "w"], dtype=object),
        }
    )
    df = df.infer_objects()

    arr_a = get_array(df, "a")
    arr_b = get_array(df, "b")
    arr_d = get_array(df, "d")

    df.iloc[0, 0] = 0
    df.iloc[0, 1] = "d"
    df.iloc[0, 3] = Timestamp("2018-12-31")
    assert np.shares_memory(arr_a, get_array(df, "a"))
    if using_infer_string and HAS_PYARROW:
        # note that the underlying memory of arr_b has been copied anyway
        # because of the assignment, but the EA is updated inplace so still
        # appears the share memory
        assert tm.shares_memory(arr_b, get_array(df, "b"))
    else:
        # TODO(CoW): Block splitting causes references here
        assert not np.shares_memory(arr_b, get_array(df, "b"))
    assert np.shares_memory(arr_d, get_array(df, "d"))

