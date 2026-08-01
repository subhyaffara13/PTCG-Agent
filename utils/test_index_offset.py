
def test_index_offset(arr, args, ret):
    assert m.index_at(arr, *args) == ret
    assert m.index_at_t(arr, *args) == ret
    assert m.offset_at(arr, *args) == ret * arr.dtype.itemsize
    assert m.offset_at_t(arr, *args) == ret * arr.dtype.itemsize

