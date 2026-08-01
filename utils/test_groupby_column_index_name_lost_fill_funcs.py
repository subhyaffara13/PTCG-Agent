
def test_groupby_column_index_name_lost_fill_funcs(func):
    # GH: 29764 groupby loses index sometimes
    df = DataFrame(
        [[1, 1.0, -1.0], [1, np.nan, np.nan], [1, 2.0, -2.0]],
        columns=Index(["type", "a", "b"], name="idx"),
    )
    df_grouped = df.groupby(["type"])[["a", "b"]]
    result = getattr(df_grouped, func)().columns
    expected = Index(["a", "b"], name="idx")
    tm.assert_index_equal(result, expected)

