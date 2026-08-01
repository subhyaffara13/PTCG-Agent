
def test_merge_antijoin_nonunique_keys():
    left = DataFrame({"A": [1.0, 2.0, 3.0], "B": ["a", "b", "b"]}).astype({"B": object})
    right = DataFrame({"C": [1.0, 2.0, 4.0], "D": ["b", "d", "d"]}).astype(
        {"D": object}
    )

    result = merge(left, right, how="left_anti", left_on="B", right_on="D")
    expected = DataFrame(
        {
            "A": [1.0],
            "B": ["a"],
            "C": [np.nan],
            "D": [np.nan],
        },
        index=[0],
    ).astype({"B": object, "D": object})
    tm.assert_frame_equal(result, expected)

    result = merge(left, right, how="right_anti", left_on="B", right_on="D")
    expected = DataFrame(
        {
            "A": [np.nan, np.nan],
            "B": [np.nan, np.nan],
            "C": [2.0, 4.0],
            "D": ["d", "d"],
        },
        index=[2, 3],
    ).astype({"B": object, "D": object})
    tm.assert_frame_equal(result, expected)

