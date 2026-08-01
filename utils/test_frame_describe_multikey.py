
def test_frame_describe_multikey(tsframe):
    grouped = tsframe.groupby([lambda x: x.year, lambda x: x.month])
    result = grouped.describe()
    desc_groups = []
    for col in tsframe:
        group = grouped[col].describe()
        # GH 17464 - Remove duplicate MultiIndex levels
        group_col = MultiIndex(
            levels=[Index([col], dtype=tsframe.columns.dtype), group.columns],
            codes=[[0] * len(group.columns), range(len(group.columns))],
        )
        group = DataFrame(group.values, columns=group_col, index=group.index)
        desc_groups.append(group)
    expected = pd.concat(desc_groups, axis=1)
    tm.assert_frame_equal(result, expected)

