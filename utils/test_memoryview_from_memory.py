
def test_memoryview_from_memory():
    view = m.test_memoryview_from_memory()
    assert isinstance(view, memoryview)
    assert view.format == "B"
    assert bytes(view) == b"\xff\xe1\xab\x37"

