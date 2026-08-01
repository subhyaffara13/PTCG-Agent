
def test_datetimelike_nonunique_index_centering(
    window, closed, expected, frame_or_series
):
    index = DatetimeIndex(
        [
            "2020-01-01",
            "2020-01-01",
            "2020-01-02",
            "2020-01-02",
            "2020-01-03",
            "2020-01-03",
            "2020-01-04",
            "2020-01-04",
        ]
    )

    df = frame_or_series([1] * 8, index=index, dtype=float)
    expected = frame_or_series(expected, index=index, dtype=float)

    result = df.rolling(window, center=True, closed=closed).sum()

    tm.assert_equal(result, expected)

