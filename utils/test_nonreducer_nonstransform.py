
def test_nonreducer_nonstransform():
    # GH3380, GH60619
    # Was originally testing mutating in a UDF; now kept as an example
    # of using apply with a nonreducer and nontransformer.
    df = DataFrame(
        {
            "cat1": ["a"] * 8 + ["b"] * 6,
            "cat2": ["c"] * 2
            + ["d"] * 2
            + ["e"] * 2
            + ["f"] * 2
            + ["c"] * 2
            + ["d"] * 2
            + ["e"] * 2,
            "val": np.random.default_rng(2).integers(100, size=14),
        }
    )

    def f(x):
        x = x.copy()
        x["rank"] = x.val.rank(method="min")
        return x.groupby("cat2")["rank"].min()

    expected = DataFrame(
        {
            "cat1": list("aaaabbb"),
            "cat2": list("cdefcde"),
            "rank": [3.0, 2.0, 5.0, 1.0, 2.0, 4.0, 1.0],
        }
    ).set_index(["cat1", "cat2"])["rank"]
    result = df.groupby("cat1").apply(f)
    tm.assert_series_equal(result, expected)

