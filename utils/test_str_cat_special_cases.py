
def test_str_cat_special_cases():
    s = Series(["a", "b", "c", "d"])
    t = Series(["d", "a", "e", "b"], index=[3, 0, 4, 1])

    # iterator of elements with different types
    expected = Series(["aaa", "bbb", "c-c", "ddd", "-e-"])
    result = s.str.cat(iter([t, s.values]), join="outer", na_rep="-")
    tm.assert_series_equal(result, expected)

    # right-align with different indexes in others
    expected = Series(["aa-", "d-d"], index=[0, 3])
    result = s.str.cat([t.loc[[0]], t.loc[[3]]], join="right", na_rep="-")
    tm.assert_series_equal(result, expected)

