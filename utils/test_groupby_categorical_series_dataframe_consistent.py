
def test_groupby_categorical_series_dataframe_consistent(df_cat):
    # GH 20416
    expected = df_cat.groupby(["A", "B"], observed=False)["C"].mean()
    result = df_cat.groupby(["A", "B"], observed=False).mean()["C"]
    tm.assert_series_equal(result, expected)

