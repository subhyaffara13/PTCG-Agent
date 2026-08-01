
def test_drop_duplicates_set():
    # GH#59237
    df = DataFrame(
        {
            "AAA": ["foo", "bar", "foo", "bar", "foo", "bar", "bar", "foo"],
            "B": ["one", "one", "two", "two", "two", "two", "one", "two"],
            "C": [1, 1, 2, 2, 2, 2, 1, 2],
            "D": range(8),
        }
    )
    # single column
    result = df.drop_duplicates({"AAA"})
    expected = df[:2]
    tm.assert_frame_equal(result, expected)

    result = df.drop_duplicates({"AAA"}, keep="last")
    expected = df.loc[[6, 7]]
    tm.assert_frame_equal(result, expected)

    result = df.drop_duplicates({"AAA"}, keep=False)
    expected = df.loc[[]]
    tm.assert_frame_equal(result, expected)
    assert len(result) == 0

    # multi column
    expected = df.loc[[0, 1, 2, 3]]
    result = df.drop_duplicates({"AAA", "B"})
    tm.assert_frame_equal(result, expected)

    result = df.drop_duplicates({"AAA", "B"}, keep="last")
    expected = df.loc[[0, 5, 6, 7]]
    tm.assert_frame_equal(result, expected)

    result = df.drop_duplicates({"AAA", "B"}, keep=False)
    expected = df.loc[[0]]
    tm.assert_frame_equal(result, expected)

