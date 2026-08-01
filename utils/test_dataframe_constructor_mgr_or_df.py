
def test_dataframe_constructor_mgr_or_df(columns, use_mgr):
    df = DataFrame({"a": [1, 2, 3]})
    df_orig = df.copy()

    if use_mgr:
        data = df._mgr
        warn = DeprecationWarning
    else:
        data = df
        warn = None
    msg = "Passing a BlockManager to DataFrame"
    with tm.assert_produces_warning(warn, match=msg, check_stacklevel=False):
        new_df = DataFrame(data)

    assert np.shares_memory(get_array(df, "a"), get_array(new_df, "a"))
    new_df.iloc[0] = 100

    assert not np.shares_memory(get_array(df, "a"), get_array(new_df, "a"))
    tm.assert_frame_equal(df, df_orig)

