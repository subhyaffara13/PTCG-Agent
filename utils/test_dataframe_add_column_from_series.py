
def test_dataframe_add_column_from_series(backend):
    # Case: adding a new column to a DataFrame from an existing column/series
    # -> delays copy under CoW
    _, DataFrame, Series = backend
    df = DataFrame({"a": [1, 2, 3], "b": [0.1, 0.2, 0.3]})

    s = Series([10, 11, 12])
    df["new"] = s
    assert np.shares_memory(get_array(df, "new"), get_array(s))

    # editing series -> doesn't modify column in frame
    s[0] = 0
    expected = DataFrame({"a": [1, 2, 3], "b": [0.1, 0.2, 0.3], "new": [10, 11, 12]})
    tm.assert_frame_equal(df, expected)

