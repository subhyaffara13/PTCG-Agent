
def test_loc_getitem_index_differently_ordered_slice_none_duplicates(indexer):
    # GH#40978
    df = DataFrame(
        [1] * 8,
        index=MultiIndex.from_tuples(
            [(1, 1), (1, 2), (1, 7), (1, 6), (2, 2), (2, 3), (2, 8), (2, 7)]
        ),
        columns=["a"],
    )
    result = df.loc[(slice(None), indexer), :]
    expected = DataFrame(
        [1] * 8,
        index=[[1, 1, 2, 1, 2, 1, 2, 2], [1, 2, 2, 7, 7, 6, 3, 8]],
        columns=["a"],
    )
    tm.assert_frame_equal(result, expected)

    result = df.loc[df.index.isin(indexer, level=1), :]
    tm.assert_frame_equal(result, df)

