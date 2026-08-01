
def test_variable_window_nonunique(closed, expected, frame_or_series):
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

    result = df.rolling("2D", closed=closed).sum()

    tm.assert_equal(result, expected)

