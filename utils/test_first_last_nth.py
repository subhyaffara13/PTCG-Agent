
def test_first_last_nth(df):
    # tests for first / last / nth
    grouped = df.groupby("A")
    first = grouped.first()
    expected = df.loc[[1, 0], ["B", "C", "D"]]
    expected.index = Index(["bar", "foo"], name="A")
    expected = expected.sort_index()
    tm.assert_frame_equal(first, expected)

    nth = grouped.nth(0)
    expected = df.loc[[0, 1]]
    tm.assert_frame_equal(nth, expected)

    last = grouped.last()
    expected = df.loc[[5, 7], ["B", "C", "D"]]
    expected.index = Index(["bar", "foo"], name="A")
    tm.assert_frame_equal(last, expected)

    nth = grouped.nth(-1)
    expected = df.iloc[[5, 7]]
    tm.assert_frame_equal(nth, expected)

    nth = grouped.nth(1)
    expected = df.iloc[[2, 3]]
    tm.assert_frame_equal(nth, expected)

    # it works!
    grouped["B"].first()
    grouped["B"].last()
    grouped["B"].nth(0)

    df = df.copy()
    df.loc[df["A"] == "foo", "B"] = np.nan
    grouped = df.groupby("A")
    assert isna(grouped["B"].first()["foo"])
    assert isna(grouped["B"].last()["foo"])
    assert isna(grouped["B"].nth(0).iloc[0])

    # v0.14.0 whatsnew
    df = DataFrame([[1, np.nan], [1, 4], [5, 6]], columns=["A", "B"])
    g = df.groupby("A")
    result = g.first()
    expected = df.iloc[[1, 2]].set_index("A")
    tm.assert_frame_equal(result, expected)

    expected = df.iloc[[1, 2]]
    result = g.nth(0, dropna="any")
    tm.assert_frame_equal(result, expected)

