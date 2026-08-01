
def test_memoryview_from_buffer_empty_shape():
    view = m.test_memoryview_from_buffer_empty_shape()
    assert isinstance(view, memoryview)
    assert view.format == "B"
    assert bytes(view) == b""

