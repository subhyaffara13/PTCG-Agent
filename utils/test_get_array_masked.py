
def test_get_array_masked():
    df = DataFrame({"a": [1, 2, 3]}, dtype="Int64")
    assert np.shares_memory(get_array(df, "a"), get_array(df, "a"))

