
def test_list_getitem_index():
    # GH 58425
    ser = Series(
        [[1, 2, 3], [4, None, 5], None],
        dtype=ArrowDtype(pa.list_(pa.int64())),
        index=[1, 3, 7],
        name="a",
    )
    actual = ser.list[1]
    expected = Series(
        [2, None, None],
        dtype="int64[pyarrow]",
        index=[1, 3, 7],
        name="a",
    )
    tm.assert_series_equal(actual, expected)

