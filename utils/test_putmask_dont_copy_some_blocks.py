
def test_putmask_dont_copy_some_blocks(val, exp, raises: bool):
    df = DataFrame({"a": [1, 2], "b": 1, "c": 1.5})
    view = df[:]
    df_orig = df.copy()
    indexer = DataFrame(
        [[True, False, False], [True, False, False]], columns=list("abc")
    )
    if raises:
        with pytest.raises(TypeError, match="Invalid value"):
            df[indexer] = val
    else:
        df[indexer] = val
        assert not np.shares_memory(get_array(view, "a"), get_array(df, "a"))
        # TODO(CoW): Could split blocks to avoid copying the whole block
        assert np.shares_memory(get_array(view, "b"), get_array(df, "b")) is exp
        assert np.shares_memory(get_array(view, "c"), get_array(df, "c"))
        assert df._mgr._has_no_reference(1) is not exp
        assert not df._mgr._has_no_reference(2)
        tm.assert_frame_equal(view, df_orig)

