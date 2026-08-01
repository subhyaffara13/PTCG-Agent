
def test_groupby_fill_duplicate_column_names(func):
    # GH: 25610 ValueError with duplicate column names
    df1 = DataFrame({"field1": [1, 3, 4], "field2": [1, 3, 4]})
    df2 = DataFrame({"field1": [1, np.nan, 4]})
    df_grouped = pd.concat([df1, df2], axis=1).groupby(by=["field2"])
    expected = DataFrame(
        [[1, 1.0], [3, np.nan], [4, 4.0]], columns=["field1", "field1"]
    )
    result = getattr(df_grouped, func)()
    tm.assert_frame_equal(result, expected)

