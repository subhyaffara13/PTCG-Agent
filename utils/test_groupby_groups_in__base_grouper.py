
def test_groupby_groups_in_BaseGrouper():
    # GH 26326
    # Test if DataFrame grouped with a pandas.Grouper has correct groups
    mi = MultiIndex.from_product([["A", "B"], ["C", "D"]], names=["alpha", "beta"])
    df = DataFrame({"foo": [1, 2, 1, 2], "bar": [1, 2, 3, 4]}, index=mi)
    result = df.groupby([Grouper(level="alpha"), "beta"])
    expected = df.groupby(["alpha", "beta"])
    assert result.groups == expected.groups

    result = df.groupby(["beta", Grouper(level="alpha")])
    expected = df.groupby(["beta", "alpha"])
    assert result.groups == expected.groups

