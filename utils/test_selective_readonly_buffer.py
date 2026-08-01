
def test_selective_readonly_buffer():
    buf = m.BufferReadOnlySelect()

    memoryview(buf)[0] = 0x64
    assert buf.value == 0x64

    io.BytesIO(b"A").readinto(buf)
    assert buf.value == ord(b"A")

    buf.readonly = True
    with pytest.raises(TypeError):
        memoryview(buf)[0] = 0
    with pytest.raises(TypeError):
        io.BytesIO(b"1").readinto(buf)

