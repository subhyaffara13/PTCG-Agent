
def test_ctypes_array_1d():
    char1d = (ctypes.c_char * 10)()
    int1d = (ctypes.c_int * 15)()
    long1d = (ctypes.c_long * 7)()

    for carray in (char1d, int1d, long1d):
        info = m.get_buffer_info(carray)
        assert info.itemsize == ctypes.sizeof(carray._type_)
        assert info.size == len(carray)
        assert info.ndim == 1
        assert info.shape == [info.size]
        assert info.strides == [info.itemsize]
        assert not info.readonly

