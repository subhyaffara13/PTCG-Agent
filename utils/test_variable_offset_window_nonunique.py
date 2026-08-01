
def test_variable_offset_window_nonunique(closed, expected, frame_or_series):
    # GH 20712
    index = DatetimeIndex(
        [
            "2011-01-01",
            "2011-01-01",
            "2011-01-02",
            "2011-01-02",
            "2011-01-02",
            "2011-01-03",
            "2011-01-04",
            "2011-01-04",
            "2011-01-05",
            "2011-01-06",
        ]
    )

    df = frame_or_series(range(10), index=index, dtype=float)
    expected = frame_or_series(expected, index=index, dtype=float)

    offset = BusinessDay(2)
    indexer = VariableOffsetWindowIndexer(index=index, offset=offset)
    result = df.rolling(indexer, closed=closed, min_periods=1).sum()

    tm.assert_equal(result, expected)

