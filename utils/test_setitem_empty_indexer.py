
def test_setitem_empty_indexer(indexer, val):
    # GH#45981
    df = DataFrame({"a": [1, 2], **val})
    expected = df.copy()
    df.loc[indexer] = 1.5
    tm.assert_frame_equal(df, expected)

