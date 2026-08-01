
def test_consolidate():
    # create unconsolidated DataFrame
    df = DataFrame({"a": [1, 2, 3], "b": [0.1, 0.2, 0.3]})
    df["c"] = [4, 5, 6]

    # take a viewing subset
    subset = df[:]

    # each block of subset references a block of df
    assert all(blk.refs.has_reference() for blk in subset._mgr.blocks)

    # consolidate the two int64 blocks
    subset._consolidate_inplace()

    # the float64 block still references the parent one because it still a view
    assert subset._mgr.blocks[0].refs.has_reference()
    # equivalent of assert np.shares_memory(df["b"].values, subset["b"].values)
    # but avoids caching df["b"]
    assert np.shares_memory(get_array(df, "b"), get_array(subset, "b"))

    # the new consolidated int64 block does not reference another
    assert not subset._mgr.blocks[1].refs.has_reference()

    # the parent dataframe now also only is linked for the float column
    assert not df._mgr.blocks[0].refs.has_reference()
    assert df._mgr.blocks[1].refs.has_reference()
    assert not df._mgr.blocks[2].refs.has_reference()

    # and modifying subset still doesn't modify parent
    subset.iloc[0, 1] = 0.0
    assert not df._mgr.blocks[1].refs.has_reference()
    assert df.loc[0, "b"] == 0.1

