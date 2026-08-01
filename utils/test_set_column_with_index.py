
def test_set_column_with_index():
    # Case: setting an index as a new column (df[col] = idx) copies that data
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    idx = Index([1, 2, 3])

    df["c"] = idx

    # the index data is copied
    assert not np.shares_memory(get_array(df, "c"), idx.values)

    idx = RangeIndex(1, 4)
    arr = idx.values

    df["d"] = idx

    assert not np.shares_memory(get_array(df, "d"), arr)

