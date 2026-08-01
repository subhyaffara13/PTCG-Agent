
def test_tuple_as_grouping():
    # https://github.com/pandas-dev/pandas/issues/18314
    df = DataFrame(
        {
            ("a", "b"): [1, 1, 1, 1],
            "a": [2, 2, 2, 2],
            "b": [2, 2, 2, 2],
            "c": [1, 1, 1, 1],
        }
    )

    with pytest.raises(KeyError, match=r"('a', 'b')"):
        df[["a", "b", "c"]].groupby(("a", "b"))

    result = df.groupby(("a", "b"))["c"].sum()
    expected = Series([4], name="c", index=Index([1], name=("a", "b")))
    tm.assert_series_equal(result, expected)

