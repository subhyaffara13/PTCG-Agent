
def test_ctypes_from_buffer():
    test_pystr = b"0123456789"
    for pyarray in (test_pystr, bytearray(test_pystr)):
        pyinfo = m.get_buffer_info(pyarray)

        if pyinfo.readonly:
            cbytes = (ctypes.c_char * len(pyarray)).from_buffer_copy(pyarray)
            cinfo = m.get_buffer_info(cbytes)
        else:
            cbytes = (ctypes.c_char * len(pyarray)).from_buffer(pyarray)
            cinfo = m.get_buffer_info(cbytes)

        assert cinfo.size == pyinfo.size
        assert cinfo.ndim == pyinfo.ndim
        assert cinfo.shape == pyinfo.shape
        assert cinfo.strides == pyinfo.strides
        assert not cinfo.readonly

