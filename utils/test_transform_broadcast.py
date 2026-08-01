
def test_transform_broadcast(tsframe, ts):
    grouped = ts.groupby(lambda x: x.month)
    result = grouped.transform(np.mean)

    tm.assert_index_equal(result.index, ts.index)
    for _, gp in grouped:
        assert_fp_equal(result.reindex(gp.index), gp.mean())

    grouped = tsframe.groupby(lambda x: x.month)
    result = grouped.transform(np.mean)
    tm.assert_index_equal(result.index, tsframe.index)
    for _, gp in grouped:
        agged = gp.mean(axis=0)
        res = result.reindex(gp.index)
        for col in tsframe:
            assert_fp_equal(res[col], agged[col])

