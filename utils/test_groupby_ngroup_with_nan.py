
def test_groupby_ngroup_with_nan():
    # GH#50100
    df = DataFrame({"a": Categorical([np.nan]), "b": [1]})
    result = df.groupby(["a", "b"], dropna=False, observed=False).ngroup()
    expected = Series([0])
    tm.assert_series_equal(result, expected)

