
def test_unstack_sort_false(frame_or_series, dtype):
    # GH 15105
    index = MultiIndex.from_tuples(
        [("two", "z", "b"), ("two", "y", "a"), ("one", "z", "b"), ("one", "y", "a")]
    )
    obj = frame_or_series(np.arange(1.0, 5.0), index=index, dtype=dtype)

    result = obj.unstack(level=0, sort=False)

    if frame_or_series is DataFrame:
        expected_columns = MultiIndex.from_tuples([(0, "two"), (0, "one")])
    else:
        expected_columns = ["two", "one"]
    expected = DataFrame(
        [[1.0, 3.0], [2.0, 4.0]],
        index=MultiIndex.from_tuples([("z", "b"), ("y", "a")]),
        columns=expected_columns,
        dtype=dtype,
    )
    tm.assert_frame_equal(result, expected)

    result = obj.unstack(level=-1, sort=False)

    if frame_or_series is DataFrame:
        expected_columns = MultiIndex(
            levels=[range(1), ["b", "a"]], codes=[[0, 0], [0, 1]]
        )
    else:
        expected_columns = ["b", "a"]

    item = pd.NA if dtype == "Float64" else np.nan
    expected = DataFrame(
        [[1.0, item], [item, 2.0], [3.0, item], [item, 4.0]],
        columns=expected_columns,
        index=MultiIndex.from_tuples(
            [("two", "z"), ("two", "y"), ("one", "z"), ("one", "y")]
        ),
        dtype=dtype,
    )
    tm.assert_frame_equal(result, expected)

    result = obj.unstack(level=[1, 2], sort=False)

    if frame_or_series is DataFrame:
        expected_columns = MultiIndex(
            levels=[range(1), ["z", "y"], ["b", "a"]], codes=[[0, 0], [0, 1], [0, 1]]
        )
    else:
        expected_columns = MultiIndex.from_tuples([("z", "b"), ("y", "a")])
    expected = DataFrame(
        [[1.0, 2.0], [3.0, 4.0]],
        index=["two", "one"],
        columns=expected_columns,
        dtype=dtype,
    )
    tm.assert_frame_equal(result, expected)

