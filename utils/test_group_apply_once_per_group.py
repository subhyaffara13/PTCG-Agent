
def test_group_apply_once_per_group(df, group_names):
    # GH2936, GH7739, GH10519, GH2656, GH12155, GH20084, GH21417

    # This test should ensure that a function is only evaluated
    # once per group. Previously the function has been evaluated twice
    # on the first group to check if the Cython index slider is safe to use
    # This test ensures that the side effect (append to list) is only triggered
    # once per group

    names = []
    # cannot parameterize over the functions since they need external
    # `names` to detect side effects

    def f_copy(group):
        # this takes the fast apply path
        names.append(group.name)
        return group.copy()

    def f_nocopy(group):
        # this takes the slow apply path
        names.append(group.name)
        return group

    def f_scalar(group):
        # GH7739, GH2656
        names.append(group.name)
        return 0

    def f_none(group):
        # GH10519, GH12155, GH21417
        names.append(group.name)

    def f_constant_df(group):
        # GH2936, GH20084
        names.append(group.name)
        return DataFrame({"a": [1], "b": [1]})

    for func in [f_copy, f_nocopy, f_scalar, f_none, f_constant_df]:
        del names[:]

        df.groupby("a").apply(func)
        assert names == group_names

