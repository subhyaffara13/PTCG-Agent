
def test_zero_byte_string():
    # Tests hack to allow chars of non-zero length, but 0 bytes
    # make reader-like thing
    str_io = BytesIO()
    r = _make_readerlike(str_io, boc.native_code)
    c_reader = m5u.VarReader5(r)
    tag_dt = np.dtype([('mdtype', 'u4'), ('byte_count', 'u4')])
    tag = np.zeros((1,), dtype=tag_dt)
    tag['mdtype'] = mio5p.miINT8
    tag['byte_count'] = 1
    hdr = m5u.VarHeader5()
    # Try when string is 1 length
    hdr.set_dims([1,])
    _write_stream(str_io, tag.tobytes() + b'        ')
    str_io.seek(0)
    val = c_reader.read_char(hdr)
    assert_equal(val, ' ')
    # Now when string has 0 bytes 1 length
    tag['byte_count'] = 0
    _write_stream(str_io, tag.tobytes())
    str_io.seek(0)
    val = c_reader.read_char(hdr)
    assert_equal(val, ' ')
    # Now when string has 0 bytes 4 length
    str_io.seek(0)
    hdr.set_dims([4,])
    val = c_reader.read_char(hdr)
    assert_array_equal(val, [' '] * 4)

