
def test_reset_index_with_empty_frame(columns):
    # Currently empty DataFrame has RangeIndex or object dtype Index, but when
    # resetting the index we still want to end up with the default string dtype
    # https://github.com/pandas-dev/pandas/issues/60338

    index = Index([], name="foo")
    df = DataFrame(index=index, columns=columns)
    result = df.reset_index()
    expected = DataFrame(columns=["foo"])
    tm.assert_frame_equal(result, expected)

    index = Index([1, 2, 3], name="foo")
    df = DataFrame(index=index, columns=columns)
    result = df.reset_index()
    expected = DataFrame({"foo": [1, 2, 3]})
    tm.assert_frame_equal(result, expected)

    index = MultiIndex.from_tuples([], names=["foo", "bar"])
    df = DataFrame(index=index, columns=columns)
    result = df.reset_index()
    expected = DataFrame(columns=["foo", "bar"])
    tm.assert_frame_equal(result, expected)

    index = MultiIndex.from_tuples([(1, 2), (2, 3)], names=["foo", "bar"])
    df = DataFrame(index=index, columns=columns)
    result = df.reset_index()
    expected = DataFrame({"foo": [1, 2], "bar": [2, 3]})
    tm.assert_frame_equal(result, expected)

