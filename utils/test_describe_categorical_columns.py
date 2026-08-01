
def test_describe_categorical_columns():
    # GH 11558
    cats = CategoricalIndex(
        ["qux", "foo", "baz", "bar"],
        categories=["foo", "bar", "baz", "qux"],
        ordered=True,
    )
    df = DataFrame(np.random.default_rng(2).standard_normal((20, 4)), columns=cats)
    result = df.groupby([1, 2, 3, 4] * 5).describe()

    tm.assert_index_equal(result.stack().columns, cats)
    tm.assert_categorical_equal(result.stack().columns.values, cats.values)

