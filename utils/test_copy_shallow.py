
def test_copy_shallow():
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [0.1, 0.2, 0.3]})
    df_copy = df.copy(deep=False)

    # the shallow copy also makes a shallow copy of the index
    assert df_copy.index is not df.index
    assert df_copy.columns is not df.columns
    assert df_copy.index.is_(df.index)
    assert df_copy.columns.is_(df.columns)

    # the shallow copy still shares memory
    assert np.shares_memory(get_array(df_copy, "a"), get_array(df, "a"))
    assert df_copy._mgr.blocks[0].refs.has_reference()
    assert df_copy._mgr.blocks[1].refs.has_reference()

    # mutating shallow copy doesn't mutate original
    df_copy.iloc[0, 0] = 0
    assert df.iloc[0, 0] == 1
    # mutating triggered a copy-on-write -> no longer shares memory
    assert not np.shares_memory(get_array(df_copy, "a"), get_array(df, "a"))
    # but still shares memory for the other columns/blocks
    assert np.shares_memory(get_array(df_copy, "c"), get_array(df, "c"))

