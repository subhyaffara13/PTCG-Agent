
def test_object_dtype_series_set_series_element():
    # GH 48933
    s1 = Series(dtype="O", index=["a", "b"])

    s1["a"] = Series()
    s1.loc["b"] = Series()

    tm.assert_series_equal(s1.loc["a"], Series())
    tm.assert_series_equal(s1.loc["b"], Series())

    s2 = Series(dtype="O", index=["a", "b"])

    s2.iloc[1] = Series()
    tm.assert_series_equal(s2.iloc[1], Series())

