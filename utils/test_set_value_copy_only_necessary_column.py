
def test_set_value_copy_only_necessary_column(indexer_func, indexer, val, col):
    # When setting inplace, only copy column that is modified instead of the whole
    # block (by splitting the block)
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": col})
    df_orig = df.copy()
    view = df[:]

    if val == "a":
        with pytest.raises(TypeError, match="Invalid value"):
            indexer_func(df)[indexer] = val
    else:
        indexer_func(df)[indexer] = val

        assert np.shares_memory(get_array(df, "b"), get_array(view, "b"))
        assert not np.shares_memory(get_array(df, "a"), get_array(view, "a"))
        tm.assert_frame_equal(view, df_orig)

