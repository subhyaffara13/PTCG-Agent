
def test_groupby_as_index_apply_str():
    ind = Index(list("abcde"))
    df = DataFrame([[1, 2], [2, 3], [1, 4], [1, 5], [2, 6]], index=ind)
    res = df.groupby(0, as_index=False, group_keys=False).apply(lambda x: x).index
    tm.assert_index_equal(res, ind)

