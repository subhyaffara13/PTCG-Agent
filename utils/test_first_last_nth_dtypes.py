
def test_first_last_nth_dtypes():
    df = DataFrame(
        {
            "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
            "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
            "C": np.random.default_rng(2).standard_normal(8),
            "D": np.array(np.random.default_rng(2).standard_normal(8), dtype="float32"),
        }
    )
    df["E"] = True
    df["F"] = 1

    # tests for first / last / nth
    grouped = df.groupby("A")
    first = grouped.first()
    expected = df.loc[[1, 0], ["B", "C", "D", "E", "F"]]
    expected.index = Index(["bar", "foo"], name="A")
    expected = expected.sort_index()
    tm.assert_frame_equal(first, expected)

    last = grouped.last()
    expected = df.loc[[5, 7], ["B", "C", "D", "E", "F"]]
    expected.index = Index(["bar", "foo"], name="A")
    expected = expected.sort_index()
    tm.assert_frame_equal(last, expected)

    nth = grouped.nth(1)
    expected = df.iloc[[2, 3]]
    tm.assert_frame_equal(nth, expected)

