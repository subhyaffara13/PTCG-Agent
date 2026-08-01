
def test_dispatch_transform(tsframe):
    df = tsframe[::5].reindex(tsframe.index)

    grouped = df.groupby(lambda x: x.month)

    filled = grouped.ffill()
    fillit = lambda x: x.ffill()
    expected = df.groupby(lambda x: x.month).transform(fillit)
    tm.assert_frame_equal(filled, expected)

