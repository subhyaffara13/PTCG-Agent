
def test_merge_antijoin_multiindex():
    left = DataFrame(
        {
            "A": [1, 2, 3],
            "B": [4, 5, 6],
        },
        index=MultiIndex.from_tuples(
            [("a", "x"), ("b", "y"), ("c", "z")], names=["first", "second"]
        ),
    )
    right = DataFrame(
        {
            "C": [7, 8, 9],
            "D": [10, 11, 12],
        },
        index=MultiIndex.from_tuples(
            [("a", "x"), ("b", "y"), ("c", "w")], names=["first", "second"]
        ),
    )

    result = merge(left, right, how="left_anti", left_index=True, right_index=True)
    expected = DataFrame(
        {
            "A": [3],
            "B": [6],
            "C": [np.nan],
            "D": [np.nan],
        },
        index=MultiIndex.from_tuples([("c", "z")], names=["first", "second"]),
    )
    tm.assert_frame_equal(result, expected)

    result = merge(left, right, how="right_anti", left_index=True, right_index=True)
    expected = DataFrame(
        {
            "A": [np.nan],
            "B": [np.nan],
            "C": [9],
            "D": [12],
        },
        index=MultiIndex.from_tuples([("c", "w")], names=["first", "second"]),
    )
    tm.assert_frame_equal(result, expected)

