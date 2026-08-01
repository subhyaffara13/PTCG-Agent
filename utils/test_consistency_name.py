
def test_consistency_name():
    # GH 12363

    df = DataFrame(
        {
            "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
            "B": ["one", "one", "two", "two", "two", "two", "one", "two"],
            "C": np.random.default_rng(2).standard_normal(8) + 1.0,
            "D": np.arange(8),
        }
    )

    expected = df.groupby(["A"]).B.count()
    result = df.B.groupby(df.A).count()
    tm.assert_series_equal(result, expected)

