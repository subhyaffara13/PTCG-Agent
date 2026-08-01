
def test_get_array_numpy():
    df = DataFrame({"a": [1, 2, 3]})
    assert np.shares_memory(get_array(df, "a"), get_array(df, "a"))

