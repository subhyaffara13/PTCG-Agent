
def test_apply_corner_cases():
    # #535, can't use sliding iterator

    N = 10
    labels = np.random.default_rng(2).integers(0, 100, size=N)
    df = DataFrame(
        {
            "key": labels,
            "value1": np.random.default_rng(2).standard_normal(N),
            "value2": ["foo", "bar", "baz", "qux", "a"] * (N // 5),
        }
    )

    grouped = df.groupby("key", group_keys=False)

    def f(g):
        g["value3"] = g["value1"] * 2
        return g

    result = grouped.apply(f)
    assert "value3" in result

