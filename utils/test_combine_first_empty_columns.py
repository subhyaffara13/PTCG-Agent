
def test_combine_first_empty_columns():
    left = DataFrame(columns=["a", "b"])
    right = DataFrame(columns=["a", "c"])
    result = left.combine_first(right)
    expected = DataFrame(columns=["a", "b", "c"])
    tm.assert_frame_equal(result, expected)

