
def test_ctypes_array_2d():
    char2d = ((ctypes.c_char * 10) * 4)()
    int2d = ((ctypes.c_int * 15) * 3)()
    long2d = ((ctypes.c_long * 7) * 2)()

    for carray in (char2d, int2d, long2d):
        info = m.get_buffer_info(carray)
        assert info.itemsize == ctypes.sizeof(carray[0]._type_)
        assert info.size == len(carray) * len(carray[0])
        assert info.ndim == 2
        assert info.shape == [len(carray), len(carray[0])]
        assert info.strides == [info.itemsize * len(carray[0]), info.itemsize]
        assert not info.readonly

