
def test_del_frame(backend):
    # Case: deleting a column with `del` on a viewing child dataframe should
    # not modify parent + update the references
    dtype_backend, DataFrame, _ = backend
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [0.1, 0.2, 0.3]})
    df_orig = df.copy()
    df2 = df[:]

    assert np.shares_memory(get_array(df, "a"), get_array(df2, "a"))

    del df2["b"]

    assert np.shares_memory(get_array(df, "a"), get_array(df2, "a"))
    tm.assert_frame_equal(df, df_orig)
    tm.assert_frame_equal(df2, df_orig[["a", "c"]])
    df2._mgr._verify_integrity()

    df.loc[0, "b"] = 200
    assert np.shares_memory(get_array(df, "a"), get_array(df2, "a"))
    df_orig = df.copy()

    df2.loc[0, "a"] = 100
    # modifying child after deleting a column still doesn't update parent
    tm.assert_frame_equal(df, df_orig)

