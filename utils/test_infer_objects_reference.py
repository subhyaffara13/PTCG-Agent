
def test_infer_objects_reference():
    df = DataFrame(
        {
            "a": [1, 2],
            "b": Series(["x", "y"], dtype=object),
            "c": 1,
            "d": Series(
                [Timestamp("2019-12-31"), Timestamp("2020-12-31")], dtype="object"
            ),
        }
    )
    view = df[:]  # noqa: F841
    df = df.infer_objects()

    arr_a = get_array(df, "a")
    arr_b = get_array(df, "b")
    arr_d = get_array(df, "d")

    df.iloc[0, 0] = 0
    df.iloc[0, 1] = "d"
    df.iloc[0, 3] = Timestamp("2018-12-31")
    assert not np.shares_memory(arr_a, get_array(df, "a"))
    assert not np.shares_memory(arr_b, get_array(df, "b"))
    assert np.shares_memory(arr_d, get_array(df, "d"))

