
def test_column_as_series(backend):
    # Case: selecting a single column now also uses Copy-on-Write
    dtype_backend, DataFrame, Series = backend
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [0.1, 0.2, 0.3]})
    df_orig = df.copy()

    s = df["a"]

    assert s.index is not df.index
    assert np.shares_memory(get_array(s, "a"), get_array(df, "a"))

    s[0] = 0

    expected = Series([0, 2, 3], name="a")
    tm.assert_series_equal(s, expected)
    # assert not np.shares_memory(s.values, get_array(df, "a"))
    tm.assert_frame_equal(df, df_orig)
    # ensure cached series on getitem is not the changed series
    tm.assert_series_equal(df["a"], df_orig["a"])

