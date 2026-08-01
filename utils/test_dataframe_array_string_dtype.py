
def test_dataframe_array_string_dtype():
    df = DataFrame({"a": ["a", "b"]}, dtype="string[python]")
    arr = np.asarray(df)
    assert np.shares_memory(arr, get_array(df, "a"))
    assert arr.flags.writeable is False

