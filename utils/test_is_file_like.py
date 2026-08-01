
def test_is_file_like():
    class MockFile:
        pass

    is_file = inference.is_file_like

    data = StringIO("data")
    assert is_file(data)

    # No read / write attributes
    # No iterator attributes
    m = MockFile()
    assert not is_file(m)

    MockFile.write = lambda self: 0

    # Write attribute but not an iterator
    m = MockFile()
    assert not is_file(m)

    # gh-16530: Valid iterator just means we have the
    # __iter__ attribute for our purposes.
    MockFile.__iter__ = lambda self: self

    # Valid write-only file
    m = MockFile()
    assert is_file(m)

    del MockFile.write
    MockFile.read = lambda self: 0

    # Valid read-only file
    m = MockFile()
    assert is_file(m)

    # Iterator but no read / write attributes
    data = [1, 2, 3]
    assert not is_file(data)

