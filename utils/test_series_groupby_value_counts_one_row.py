
def test_series_groupby_value_counts_one_row(columns):
    # GH42618
    df = DataFrame(data=[range(len(columns))], columns=columns)
    dfg = df.groupby(columns[:-1])

    result = dfg[columns[-1]].value_counts()
    expected = df.value_counts()

    tm.assert_series_equal(result, expected)

