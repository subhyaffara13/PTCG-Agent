
def test_transpose_ea_single_column():
    df = DataFrame({"a": [1, 2, 3]}, dtype="Int64")
    result = df.T

    assert not np.shares_memory(get_array(df, "a"), get_array(result, 0))

