
def test_get_group_len_1_list_likes(test_series, kwarg, value, name, warn):
    # GH#25971
    obj = DataFrame({"b": [3, 4, 5]}, index=Index([1, 1, 2], name="a"))
    if test_series:
        obj = obj["b"]
    gb = obj.groupby(**{kwarg: value})
    result = gb.get_group(name)
    if test_series:
        expected = Series([3, 4], index=Index([1, 1], name="a"), name="b")
    else:
        expected = DataFrame({"b": [3, 4]}, index=Index([1, 1], name="a"))
    tm.assert_equal(result, expected)

