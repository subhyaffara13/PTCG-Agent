import copy

def test_dataframe_from_numpy_array(copy):
    arr = np.array([[1, 2], [3, 4]])
    df = DataFrame(arr, copy=copy)

    if copy is not False or copy is True:
        assert not np.shares_memory(get_array(df, 0), arr)
    else:
        assert np.shares_memory(get_array(df, 0), arr)

