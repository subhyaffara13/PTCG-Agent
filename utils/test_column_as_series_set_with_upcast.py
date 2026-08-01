
def test_column_as_series_set_with_upcast(backend):
    # Case: selecting a single column now also uses Copy-on-Write -> when
    # setting a value causes an upcast, we don't need to update the parent
    # DataFrame through the cache mechanism
    dtype_backend, DataFrame, Series = backend
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [0.1, 0.2, 0.3]})
    df_orig = df.copy()

    s = df["a"]
    if dtype_backend == "nullable":
        with pytest.raises(TypeError, match="Invalid value"):
            s[0] = "foo"
        expected = Series([1, 2, 3], name="a")
        tm.assert_series_equal(s, expected)
        tm.assert_frame_equal(df, df_orig)
        # ensure cached series on getitem is not the changed series
        tm.assert_series_equal(df["a"], df_orig["a"])
    else:
        with pytest.raises(TypeError, match="Invalid value"):
            s[0] = "foo"

