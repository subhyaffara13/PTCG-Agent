
def test_observed_perf():
    # we create a cartesian product, so this is
    # non-performant if we don't use observed values
    # gh-14942
    df = DataFrame(
        {
            "cat": np.random.default_rng(2).integers(0, 255, size=30000),
            "int_id": np.random.default_rng(2).integers(0, 255, size=30000),
            "other_id": np.random.default_rng(2).integers(0, 10000, size=30000),
            "foo": 0,
        }
    )
    df["cat"] = df.cat.astype(str).astype("category")

    grouped = df.groupby(["cat", "int_id", "other_id"], observed=True)
    result = grouped.count()
    assert result.index.levels[0].nunique() == df.cat.nunique()
    assert result.index.levels[1].nunique() == df.int_id.nunique()
    assert result.index.levels[2].nunique() == df.other_id.nunique()

