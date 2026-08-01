
def test_astype_string_and_object(dtype, new_dtype):
    df = DataFrame({"a": ["a", "b", "c"]}, dtype=dtype)
    df_orig = df.copy()
    df2 = df.astype(new_dtype)
    assert np.shares_memory(get_array(df2, "a"), get_array(df, "a"))

    df2.iloc[0, 0] = "x"
    tm.assert_frame_equal(df, df_orig)

