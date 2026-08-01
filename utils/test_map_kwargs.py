
def test_map_kwargs():
    # GH 59814
    result = Series([2, 4, 5]).map(lambda x, y: x + y, y=2)
    expected = Series([4, 6, 7])
    tm.assert_series_equal(result, expected)


def test_map_kwargs():
    # GH 40652
    result = DataFrame([[1, 2], [3, 4]]).map(lambda x, y: x + y, y=2)
    expected = DataFrame([[3, 4], [5, 6]])
    tm.assert_frame_equal(result, expected)

