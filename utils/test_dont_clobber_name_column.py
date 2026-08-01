
def test_dont_clobber_name_column():
    df = DataFrame(
        {"key": ["a", "a", "a", "b", "b", "b"], "name": ["foo", "bar", "baz"] * 2}
    )

    result = df.groupby("key", group_keys=False).apply(lambda x: x)
    tm.assert_frame_equal(result, df[["name"]])

