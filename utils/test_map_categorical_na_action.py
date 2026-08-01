
def test_map_categorical_na_action(na_action, expected):
    dtype = pd.CategoricalDtype(list("DCBA"), ordered=True)
    values = pd.Categorical([*list("AB"), np.nan], dtype=dtype)
    s = Series(values, name="XX")
    result = s.map(str, na_action=na_action)
    tm.assert_series_equal(result, expected)

