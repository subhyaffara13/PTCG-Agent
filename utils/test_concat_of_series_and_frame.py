
def test_concat_of_series_and_frame(inputs, ignore_index, axis, expected):
    # GH #60723 and #56257
    result = concat(inputs, ignore_index=ignore_index, axis=axis)
    tm.assert_frame_equal(result, expected)

