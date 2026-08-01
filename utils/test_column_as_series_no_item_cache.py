
def test_column_as_series_no_item_cache(request, backend, method):
    # Case: selecting a single column (which now also uses Copy-on-Write to protect
    # the view) should always give a new object (i.e. not make use of a cache)
    dtype_backend, DataFrame, _ = backend
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [0.1, 0.2, 0.3]})
    df_orig = df.copy()

    s1 = method(df)
    s2 = method(df)

    assert s1 is not s2
    assert s1.index is not df.index
    assert s1.index is not s2.index

    s1.iloc[0] = 0

    tm.assert_series_equal(s2, df_orig["a"])
    tm.assert_frame_equal(df, df_orig)

