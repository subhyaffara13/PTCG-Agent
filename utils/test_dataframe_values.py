
def test_dataframe_values(method):
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    df_orig = df.copy()

    arr = method(df)

    # .values still gives a view but is read-only
    assert np.shares_memory(arr, get_array(df, "a"))
    assert arr.flags.writeable is False

    # mutating series through arr therefore doesn't work
    with pytest.raises(ValueError, match="read-only"):
        arr[0, 0] = 0
    tm.assert_frame_equal(df, df_orig)

    # mutating the series itself still works
    df.iloc[0, 0] = 0
    assert df.values[0, 0] == 0

