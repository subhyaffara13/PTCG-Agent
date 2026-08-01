
def test_merge_antijoin_nans():
    left = DataFrame({"A": [1.0, 2.0, np.nan], "C": ["a", "b", "c"]}).astype(
        {"C": object}
    )
    right = DataFrame({"A": [3.0, 2.0, np.nan], "D": ["d", "e", "f"]}).astype(
        {"D": object}
    )
    result = merge(left, right, how="left_anti", on="A")
    expected = DataFrame({"A": [1.0], "C": ["a"], "D": [np.nan]}).astype(
        {"C": object, "D": object}
    )
    tm.assert_frame_equal(result, expected)

