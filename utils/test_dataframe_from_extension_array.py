
def test_dataframe_from_extension_array(copy, data, dtype):
    arr = pd.array(data, dtype=dtype)
    df = DataFrame(arr, copy=copy)

    if arr.dtype == "Int64":
        # to ensure tm.shares_memory works correctly
        # TODO fix in tm.shares_memory or get_array?
        arr = arr._data

    if copy is None or copy is True:
        assert not tm.shares_memory(get_array(df, 0), arr)
    else:
        assert tm.shares_memory(get_array(df, 0), arr)

