
def test_to_frame_column_rangeindex():
    idx = pd.Index([1])
    result = idx.to_frame().columns
    expected = RangeIndex(1)
    tm.assert_index_equal(result, expected, exact=True)


def test_to_frame_column_rangeindex():
    mi = MultiIndex.from_arrays([[1, 2], ["a", "b"]])
    result = mi.to_frame().columns
    expected = RangeIndex(2)
    tm.assert_index_equal(result, expected, exact=True)

