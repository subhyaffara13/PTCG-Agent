
def test_map_categorical(na_action, using_infer_string):
    values = pd.Categorical(list("ABBABCD"), categories=list("DCBA"), ordered=True)
    s = Series(values, name="XX", index=list("abcdefg"))

    result = s.map(lambda x: x.lower(), na_action=na_action)
    exp_values = pd.Categorical(list("abbabcd"), categories=list("dcba"), ordered=True)
    exp = Series(exp_values, name="XX", index=list("abcdefg"))
    tm.assert_series_equal(result, exp)
    tm.assert_categorical_equal(result.values, exp_values)

    result = s.map(lambda x: "A", na_action=na_action)
    exp = Series(["A"] * 7, name="XX", index=list("abcdefg"))
    tm.assert_series_equal(result, exp)
    assert result.dtype == object if not using_infer_string else "str"

