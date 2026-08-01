
def test_first_fill_value_loc(arr, fill_value, loc):
    result = SparseArray(arr, fill_value=fill_value)._first_fill_value_loc()
    assert result == loc

