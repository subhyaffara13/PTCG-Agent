
def test_readonly_buffer():
    buf = m.BufferReadOnly(0x64)
    view = memoryview(buf)
    assert view[0] == 0x64
    assert view.readonly
    with pytest.raises(TypeError):
        view[0] = 0

