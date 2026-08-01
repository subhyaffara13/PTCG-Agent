
def test_list_len():
    ser = Series(
        [[1, 2, 3], [4, None], None],
        dtype=ArrowDtype(pa.list_(pa.int64())),
        name="a",
    )
    actual = ser.list.len()
    expected = Series([3, 2, None], dtype=ArrowDtype(pa.int32()), name="a")
    tm.assert_series_equal(actual, expected)

