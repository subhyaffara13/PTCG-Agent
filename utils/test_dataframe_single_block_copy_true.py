
def test_dataframe_single_block_copy_true():
    # the copy=False/None cases are tested above in test_dataframe_values
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    arr = np.array(df, copy=True)
    assert not np.shares_memory(arr, get_array(df, "a"))
    assert arr.flags.writeable is True

