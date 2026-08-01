
def test_stack_sort_false(future_stack):
    # GH 15105
    data = [[1, 2, 3.0, 4.0], [2, 3, 4.0, 5.0], [3, 4, np.nan, np.nan]]
    df = DataFrame(
        data,
        columns=MultiIndex(
            levels=[["B", "A"], ["x", "y"]], codes=[[0, 0, 1, 1], [0, 1, 0, 1]]
        ),
    )
    kwargs = {} if future_stack else {"sort": False}
    result = df.stack(level=0, future_stack=future_stack, **kwargs)
    if future_stack:
        expected = DataFrame(
            {
                "x": [1.0, 3.0, 2.0, 4.0, 3.0, np.nan],
                "y": [2.0, 4.0, 3.0, 5.0, 4.0, np.nan],
            },
            index=MultiIndex.from_arrays(
                [[0, 0, 1, 1, 2, 2], ["B", "A", "B", "A", "B", "A"]]
            ),
        )
    else:
        expected = DataFrame(
            {"x": [1.0, 3.0, 2.0, 4.0, 3.0], "y": [2.0, 4.0, 3.0, 5.0, 4.0]},
            index=MultiIndex.from_arrays([[0, 0, 1, 1, 2], ["B", "A", "B", "A", "B"]]),
        )
    tm.assert_frame_equal(result, expected)

    # Codes sorted in this call
    df = DataFrame(
        data,
        columns=MultiIndex.from_arrays([["B", "B", "A", "A"], ["x", "y", "x", "y"]]),
    )
    kwargs = {} if future_stack else {"sort": False}
    result = df.stack(level=0, future_stack=future_stack, **kwargs)
    tm.assert_frame_equal(result, expected)

