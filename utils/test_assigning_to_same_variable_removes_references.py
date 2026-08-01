
def test_assigning_to_same_variable_removes_references():
    df = DataFrame({"a": [1, 2, 3]})
    df = df.reset_index()
    assert df._mgr._has_no_reference(1)
    arr = get_array(df, "a")
    df.iloc[0, 1] = 100  # Write into a

    assert np.shares_memory(arr, get_array(df, "a"))

