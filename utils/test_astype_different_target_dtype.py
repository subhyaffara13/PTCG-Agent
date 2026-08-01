
def test_astype_different_target_dtype(dtype):
    if dtype == "int32[pyarrow]":
        pytest.importorskip("pyarrow")
    df = DataFrame({"a": [1, 2, 3]})
    df_orig = df.copy()
    df2 = df.astype(dtype)

    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    assert df2._mgr._has_no_reference(0)

    df2.iloc[0, 0] = 5
    tm.assert_frame_equal(df, df_orig)

    # mutating parent also doesn't update result
    df2 = df.astype(dtype)
    df.iloc[0, 0] = 100
    tm.assert_frame_equal(df2, df_orig.astype(dtype))

