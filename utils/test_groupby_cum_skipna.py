
def test_groupby_cum_skipna(op, skipna, input, exp):
    df = DataFrame(input)
    result = df.groupby("key")["value"].transform(op, skipna=skipna)
    if isinstance(exp, dict):
        expected = exp[(op, skipna)]
    else:
        expected = exp
    expected = Series(expected, name="value")
    tm.assert_series_equal(expected, result)

