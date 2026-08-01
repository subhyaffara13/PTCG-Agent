
def test_read_csv_file_handle(all_parsers, io_class, encoding):
    """
    Test whether read_csv does not close user-provided file handles.

    GH 36980
    """
    parser = all_parsers
    expected = DataFrame({"a": [1], "b": [2]})

    content = "a,b\n1,2"
    handle = io_class(content.encode("utf-8") if io_class == BytesIO else content)

    tm.assert_frame_equal(parser.read_csv(handle, encoding=encoding), expected)
    assert not handle.closed

