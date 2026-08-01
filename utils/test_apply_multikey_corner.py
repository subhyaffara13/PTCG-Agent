
def test_apply_multikey_corner(tsframe):
    grouped = tsframe.groupby([lambda x: x.year, lambda x: x.month])

    def f(group):
        return group.sort_values("A")[-5:]

    result = grouped.apply(f)
    for key, group in grouped:
        tm.assert_frame_equal(result.loc[key], f(group))

