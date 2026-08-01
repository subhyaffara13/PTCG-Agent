
def test_merge_on_all_nan_column():
    # GH#59421
    left = DataFrame({"x": [1, 2, 3], "y": [np.nan, np.nan, np.nan], "z": [4, 5, 6]})
    right = DataFrame({"x": [1, 2, 3], "y": [np.nan, np.nan, np.nan], "zz": [4, 5, 6]})
    result = left.merge(right, on=["x", "y"], how="outer")
    # Should not trigger array bounds eerror with bounds checking or asan enabled.
    expected = DataFrame(
        {"x": [1, 2, 3], "y": [np.nan, np.nan, np.nan], "z": [4, 5, 6], "zz": [4, 5, 6]}
    )
    tm.assert_frame_equal(result, expected)

