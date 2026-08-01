
def test_dataframe_array_ea_dtypes(method):
    df = DataFrame({"a": [1, 2, 3]}, dtype="Int64")
    arr = method(df)

    assert np.shares_memory(arr, get_array(df, "a"))
    assert arr.flags.writeable is False

