
def test_astype_string_and_object_update_original(dtype, new_dtype):
    df = DataFrame({"a": ["a", "b", "c"]}, dtype=dtype)
    df2 = df.astype(new_dtype)
    df_orig = df2.copy()
    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))

    df.iloc[0, 0] = "x"
    tm.assert_frame_equal(df2, df_orig)

