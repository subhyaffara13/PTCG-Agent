
def test_memoryview(method, args, fmt, expected_view):
    view = method(*args)
    assert isinstance(view, memoryview)
    assert view.format == fmt
    assert list(view) == list(expected_view)

