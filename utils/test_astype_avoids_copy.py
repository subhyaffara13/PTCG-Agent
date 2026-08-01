
def test_astype_avoids_copy(dtype, new_dtype):
    if new_dtype == "int64[pyarrow]":
        pytest.importorskip("pyarrow")
    df = DataFrame({"a": [1, 2, 3]}, dtype=dtype)
    df_orig = df.copy()
    df2 = df.astype(new_dtype)
    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))

    # mutating df2 triggers a copy-on-write for that column/block
    df2.iloc[0, 0] = 10
    assert not np.shares_memory(get_array(df2, "a"), get_array(df, "a"))
    tm.assert_frame_equal(df, df_orig)

    # mutating parent also doesn't update result
    df2 = df.astype(new_dtype)
    df.iloc[0, 0] = 100
    tm.assert_frame_equal(df2, df_orig.astype(new_dtype))

