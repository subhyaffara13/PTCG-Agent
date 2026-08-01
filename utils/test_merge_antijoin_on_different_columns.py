
def test_merge_antijoin_on_different_columns():
    left = DataFrame({"A": [1.0, 2.0, 3.0], "B": ["a", "b", "c"]}).astype({"B": object})
    right = DataFrame({"C": [1.0, 2.0, 4.0], "D": ["a", "d", "b"]}).astype(
        {"D": object}
    )

    result = merge(left, right, how="left_anti", left_on="B", right_on="D")
    expected = DataFrame(
        {
            "A": [3.0],
            "B": ["c"],
            "C": [np.nan],
            "D": [np.nan],
        },
        index=[2],
    ).astype({"B": object, "D": object})
    tm.assert_frame_equal(result, expected)

    result = merge(left, right, how="right_anti", left_on="B", right_on="D")
    expected = DataFrame(
        {
            "A": [np.nan],
            "B": [np.nan],
            "C": [2.0],
            "D": ["d"],
        },
        index=[1],
    ).astype({"B": object, "D": object})
    tm.assert_frame_equal(result, expected)

