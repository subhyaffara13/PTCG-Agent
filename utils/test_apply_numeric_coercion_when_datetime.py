
def test_apply_numeric_coercion_when_datetime():
    # In the past, group-by/apply operations have been over-eager
    # in converting dtypes to numeric, in the presence of datetime
    # columns.  Various GH issues were filed, the reproductions
    # for which are here.

    # GH 15670
    df = DataFrame(
        {"Number": [1, 2], "Date": ["2017-03-02"] * 2, "Str": ["foo", "inf"]}
    )
    expected = df.groupby(["Number"]).apply(lambda x: x.iloc[0])
    df.Date = pd.to_datetime(df.Date)
    result = df.groupby(["Number"]).apply(lambda x: x.iloc[0])
    tm.assert_series_equal(result["Str"], expected["Str"])

