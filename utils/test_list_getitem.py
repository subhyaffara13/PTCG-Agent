
def test_list_getitem(list_dtype):
    ser = Series(
        [[1, 2, 3], [4, None, 5], None],
        dtype=ArrowDtype(list_dtype),
        name="a",
    )
    actual = ser.list[1]
    expected = Series([2, None, None], dtype="int64[pyarrow]", name="a")
    tm.assert_series_equal(actual, expected)

