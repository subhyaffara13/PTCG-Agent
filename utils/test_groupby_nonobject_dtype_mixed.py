
def test_groupby_nonobject_dtype_mixed():
    # GH 3911, mixed frame non-conversion
    df = DataFrame(
        {
            "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
            "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
            "C": np.random.default_rng(2).standard_normal(8),
            "D": np.array(np.random.default_rng(2).standard_normal(8), dtype="float32"),
        }
    )
    df["value"] = range(len(df))

    def max_value(group):
        return group.loc[group["value"].idxmax()]

    applied = df.groupby("A").apply(max_value)
    result = applied.dtypes
    expected = df.drop(columns="A").dtypes
    tm.assert_series_equal(result, expected)

