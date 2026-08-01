
def test_read_stream():
    tag = _make_tag('i4', 1, mio5p.miINT32, sde=True)
    tag_str = tag.tobytes()
    str_io = BytesIO(tag_str)
    st = streams.make_stream(str_io)
    s = streams._read_into(st, tag.itemsize)
    assert_equal(s, tag.tobytes())

