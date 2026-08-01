
def test_read_numeric_writeable():
    # make reader-like thing
    str_io = BytesIO()
    r = _make_readerlike(str_io, '<')
    c_reader = m5u.VarReader5(r)
    dt = np.dtype('<u2')
    a = _make_tag(dt, 30, mio5p.miUINT16, 0)
    a_str = a.tobytes()
    _write_stream(str_io, a_str)
    el = c_reader.read_numeric()
    assert_(el.flags.writeable is True)

