
def test_series_groupby_value_counts_empty(columns):
    # GH39172
    df = DataFrame(columns=columns)
    dfg = df.groupby(columns[:-1])

    result = dfg[columns[-1]].value_counts()
    expected = Series([], dtype=result.dtype, name="count")
    expected.index = MultiIndex.from_arrays([[]] * len(columns), names=columns)

    tm.assert_series_equal(result, expected)

