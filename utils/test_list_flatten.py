
def test_list_flatten():
    ser = Series(
        [[1, 2, 3], None, [4, None], [], [7, 8]],
        dtype=ArrowDtype(pa.list_(pa.int64())),
        name="a",
    )
    actual = ser.list.flatten()
    expected = Series(
        [1, 2, 3, 4, None, 7, 8],
        dtype=ArrowDtype(pa.int64()),
        index=[0, 0, 0, 2, 2, 4, 4],
        name="a",
    )
    tm.assert_series_equal(actual, expected)

