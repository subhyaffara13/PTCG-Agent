
def test_assert_frame_equal_checking_allow_dups_flag():
    # GH#45554
    left = DataFrame([[1, 2], [3, 4]])
    left.flags.allows_duplicate_labels = False

    right = DataFrame([[1, 2], [3, 4]])
    right.flags.allows_duplicate_labels = True
    tm.assert_frame_equal(left, right, check_flags=False)

    with pytest.raises(AssertionError, match="allows_duplicate_labels"):
        tm.assert_frame_equal(left, right, check_flags=True)

