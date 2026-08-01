
def test_null_slice(backend, method):
    # Case: also all variants of indexing with a null slice (:) should return
    # new objects to ensure we correctly use CoW for the results
    dtype_backend, DataFrame, _ = backend
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})
    df_orig = df.copy()

    df2 = method(df)

    # we always return new objects (shallow copy), regardless of CoW or not
    assert df2 is not df
    assert df2.index is not df.index
    assert df2.columns is not df.columns

    # and those trigger CoW when mutated
    df2.iloc[0, 0] = 0
    tm.assert_frame_equal(df, df_orig)

