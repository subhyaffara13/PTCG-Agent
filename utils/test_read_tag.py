
def test_read_tag():
    # mainly to test errors
    # make reader-like thing
    str_io = BytesIO()
    r = _make_readerlike(str_io)
    c_reader = m5u.VarReader5(r)
    # This works for StringIO but _not_ BytesIO
    assert_raises(OSError, c_reader.read_tag)
    # bad SDE
    tag = _make_tag('i4', 1, mio5p.miINT32, sde=True)
    tag['byte_count'] = 5
    _write_stream(str_io, tag.tobytes())
    assert_raises(ValueError, c_reader.read_tag)

