
def test_non_fixed_variable_window_indexer(closed, expected_data):
    index = date_range("2020", periods=10)
    df = DataFrame(range(10), index=index)
    offset = BusinessDay(1)
    indexer = VariableOffsetWindowIndexer(index=index, offset=offset)
    result = df.rolling(indexer, closed=closed).sum()
    expected = DataFrame(expected_data, index=index)
    tm.assert_frame_equal(result, expected)

