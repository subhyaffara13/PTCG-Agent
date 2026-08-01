
def test_memoryview_refcount(method):
    buf = b"\x0a\x0b\x0c\x0d"
    ref_before = sys.getrefcount(buf)
    view = method(buf)
    ref_after = sys.getrefcount(buf)
    assert ref_before < ref_after
    assert list(view) == list(buf)

