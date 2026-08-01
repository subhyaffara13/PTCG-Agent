
def test_groups_na_category(dropna, observed):
    # https://github.com/pandas-dev/pandas/issues/61356
    df = DataFrame(
        {"cat": Categorical(["a", np.nan, "a"], categories=list("adb"))},
        index=list("xyz"),
    )
    g = df.groupby("cat", observed=observed, dropna=dropna)

    result = g.groups
    expected = {"a": Index(["x", "z"])}
    if not dropna:
        expected |= {np.nan: Index(["y"])}
    if not observed:
        expected |= {"b": Index([]), "d": Index([])}
    tm.assert_dict_equal(result, expected)

