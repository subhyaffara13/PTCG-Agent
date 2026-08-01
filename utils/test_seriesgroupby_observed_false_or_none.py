
def test_seriesgroupby_observed_false_or_none(df_cat, observed, operation):
    # GH 24880
    # GH#49223 - order of results was wrong when grouping by index levels
    index, _ = MultiIndex.from_product(
        [
            CategoricalIndex(["bar", "foo"], ordered=False),
            CategoricalIndex(["one", "three", "two"], ordered=False),
        ],
        names=["A", "B"],
    ).sortlevel()

    expected = Series(data=[2, 4, 0, 1, 0, 3], index=index, name="C")
    grouped = df_cat.groupby(["A", "B"], observed=observed)["C"]
    result = getattr(grouped, operation)(sum)
    tm.assert_series_equal(result, expected)

