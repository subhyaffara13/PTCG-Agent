
def test_observed_groups(observed):
    # gh-20583
    # test that we have the appropriate groups

    cat = Categorical(["a", "c", "a"], categories=["a", "b", "c"])
    df = DataFrame({"cat": cat, "vals": [1, 2, 3]})
    g = df.groupby("cat", observed=observed)

    result = g.groups
    if observed:
        expected = {"a": Index([0, 2], dtype="int64"), "c": Index([1], dtype="int64")}
    else:
        expected = {
            "a": Index([0, 2], dtype="int64"),
            "b": Index([], dtype="int64"),
            "c": Index([1], dtype="int64"),
        }

    tm.assert_dict_equal(result, expected)

