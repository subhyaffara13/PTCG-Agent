
def test_merge_copy_keyword():
    df = DataFrame({"a": [1, 2]})
    df2 = DataFrame({"b": [3, 4.5]})

    result = df.merge(df2, left_index=True, right_index=True)

    assert np.shares_memory(get_array(df, "a"), get_array(result, "a"))
    assert np.shares_memory(get_array(df2, "b"), get_array(result, "b"))

