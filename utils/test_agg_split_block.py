
def test_agg_split_block():
    # https://github.com/pandas-dev/pandas/issues/31522
    df = DataFrame(
        {
            "key1": ["a", "a", "b", "b", "a"],
            "key2": ["one", "two", "one", "two", "one"],
            "key3": ["three", "three", "three", "six", "six"],
        }
    )
    result = df.groupby("key1").min()
    expected = DataFrame(
        {"key2": ["one", "one"], "key3": ["six", "six"]},
        index=Index(["a", "b"], name="key1"),
    )
    tm.assert_frame_equal(result, expected)

