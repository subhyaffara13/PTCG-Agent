
def test_seriesgroupby_observed_true(df_cat, operation):
    # GH#24880
    # GH#49223 - order of results was wrong when grouping by index levels
    lev_a = Index(["bar", "bar", "foo", "foo"], dtype=df_cat["A"].dtype, name="A")
    lev_b = Index(["one", "three", "one", "two"], dtype=df_cat["B"].dtype, name="B")
    index = MultiIndex.from_arrays([lev_a, lev_b])
    expected = Series(data=[2, 4, 1, 3], index=index, name="C").sort_index()

    grouped = df_cat.groupby(["A", "B"], observed=True)["C"]
    result = getattr(grouped, operation)(sum)
    tm.assert_series_equal(result, expected)

