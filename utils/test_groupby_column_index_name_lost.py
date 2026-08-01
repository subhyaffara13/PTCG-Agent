
def test_groupby_column_index_name_lost(func):
    # GH: 29764 groupby loses index sometimes
    expected = Index(["a"], name="idx")
    df = DataFrame([[1]], columns=expected)
    df_grouped = df.groupby([1])
    result = getattr(df_grouped, func)().columns
    tm.assert_index_equal(result, expected)

