
def test_join_empty_uncomparable_columns():
    # GH 57048
    df1 = DataFrame()
    df2 = DataFrame(columns=["test"])
    df3 = DataFrame(columns=["foo", ("bar", "baz")])

    result = df1 + df2
    expected = DataFrame(columns=["test"])
    tm.assert_frame_equal(result, expected)

    result = df2 + df3
    expected = DataFrame(columns=[("bar", "baz"), "foo", "test"])
    tm.assert_frame_equal(result, expected)

    result = df1 + df3
    expected = DataFrame(columns=[("bar", "baz"), "foo"])
    tm.assert_frame_equal(result, expected)

