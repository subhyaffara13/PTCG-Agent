
def test_allows_duplicate_labels():
    left = DataFrame()
    right = DataFrame().set_flags(allows_duplicate_labels=False)
    tm.assert_frame_equal(left, left)
    tm.assert_frame_equal(right, right)
    tm.assert_frame_equal(left, right, check_flags=False)
    tm.assert_frame_equal(right, left, check_flags=False)

    with pytest.raises(AssertionError, match="<Flags"):
        tm.assert_frame_equal(left, right)

    with pytest.raises(AssertionError, match="<Flags"):
        tm.assert_frame_equal(left, right)


def test_allows_duplicate_labels():
    left = Series([1])
    right = Series([1]).set_flags(allows_duplicate_labels=False)
    tm.assert_series_equal(left, left)
    tm.assert_series_equal(right, right)
    tm.assert_series_equal(left, right, check_flags=False)
    tm.assert_series_equal(right, left, check_flags=False)

    with pytest.raises(AssertionError, match="<Flags"):
        tm.assert_series_equal(left, right)

    with pytest.raises(AssertionError, match="<Flags"):
        tm.assert_series_equal(left, right)

