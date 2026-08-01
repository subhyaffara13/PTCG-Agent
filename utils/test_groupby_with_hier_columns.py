
def test_groupby_with_hier_columns():
    tuples = list(
        zip(
            *[
                ["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"],
                ["one", "two", "one", "two", "one", "two", "one", "two"],
            ],
            strict=True,
        )
    )
    index = MultiIndex.from_tuples(tuples)
    columns = MultiIndex.from_tuples(
        [("A", "cat"), ("B", "dog"), ("B", "cat"), ("A", "dog")]
    )
    df = DataFrame(
        np.random.default_rng(2).standard_normal((8, 4)), index=index, columns=columns
    )

    result = df.groupby(level=0).mean()
    tm.assert_index_equal(result.columns, columns)

    result = df.groupby(level=0).agg("mean")
    tm.assert_index_equal(result.columns, columns)

    result = df.groupby(level=0).apply(lambda x: x.mean())
    tm.assert_index_equal(result.columns, columns)

    # add a nuisance column
    sorted_columns, _ = columns.sortlevel(0)
    df["A", "foo"] = "bar"
    result = df.groupby(level=0).mean(numeric_only=True)
    tm.assert_index_equal(result.columns, df.columns[:-1])

