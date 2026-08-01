
def test_filter_using_len():
    # GH 4447
    df = DataFrame({"A": np.arange(8), "B": list("aabbbbcc"), "C": np.arange(8)})
    grouped = df.groupby("B")
    actual = grouped.filter(lambda x: len(x) > 2)
    expected = DataFrame(
        {"A": np.arange(2, 6), "B": list("bbbb"), "C": np.arange(2, 6)},
        index=range(2, 6),
    )
    tm.assert_frame_equal(actual, expected)

    actual = grouped.filter(lambda x: len(x) > 4)
    expected = df.loc[[]]
    tm.assert_frame_equal(actual, expected)

