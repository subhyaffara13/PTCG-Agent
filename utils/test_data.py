
def test_data(arr, args, ret):
    from sys import byteorder

    assert all(m.data_t(arr, *args) == ret)
    assert all(m.data(arr, *args)[(0 if byteorder == "little" else 1) :: 2] == ret)
    assert all(m.data(arr, *args)[(1 if byteorder == "little" else 0) :: 2] == 0)

