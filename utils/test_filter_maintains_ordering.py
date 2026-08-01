
def test_filter_maintains_ordering(index):
    # GH 4621
    df = DataFrame(
        {"pid": [1, 1, 1, 2, 2, 3, 3, 3], "tag": [23, 45, 62, 24, 45, 34, 25, 62]},
        index=index,
    )
    s = df["pid"]
    grouped = df.groupby("tag")
    actual = grouped.filter(lambda x: len(x) > 1)
    expected = df.iloc[[1, 2, 4, 7]]
    tm.assert_frame_equal(actual, expected)

    grouped = s.groupby(df["tag"])
    actual = grouped.filter(lambda x: len(x) > 1)
    expected = s.iloc[[1, 2, 4, 7]]
    tm.assert_series_equal(actual, expected)

