
def test_file_handle_string_io(all_parsers):
    # gh-14418
    #
    # Don't close user provided file handles.
    parser = all_parsers
    data = "a,b\n1,2"

    fh = StringIO(data)
    parser.read_csv(fh)
    assert not fh.closed

