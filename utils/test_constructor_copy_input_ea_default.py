
def test_constructor_copy_input_ea_default():
    arr = array([0, 1], dtype="Int64")
    idx = Index(arr)
    assert not tm.shares_memory(arr, idx.array)

