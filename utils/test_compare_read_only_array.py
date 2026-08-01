
def test_compare_read_only_array():
    # GH#57130
    arr = np.array([], dtype=object)
    arr.flags.writeable = False
    idx = pd.Index(arr)
    result = idx > 69
    assert result.dtype == bool

