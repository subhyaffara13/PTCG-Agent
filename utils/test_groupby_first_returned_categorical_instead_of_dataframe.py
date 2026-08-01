
def test_groupby_first_returned_categorical_instead_of_dataframe(func):
    # GH 28641: groupby drops index, when grouping over categorical column with
    # first/last. Renamed Categorical instead of DataFrame previously.
    df = DataFrame({"A": [1997], "B": Series(["b"], dtype="category").cat.as_ordered()})
    df_grouped = df.groupby("A")["B"]
    result = getattr(df_grouped, func)()

    # ordered categorical dtype should be preserved
    expected = Series(
        ["b"], index=Index([1997], name="A"), name="B", dtype=df["B"].dtype
    )
    tm.assert_series_equal(result, expected)

