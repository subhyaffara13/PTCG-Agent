
def test_file_handles_mmap(c_parser_only, csv1):
    # gh-14418
    #
    # Don't close user provided file handles.
    parser = c_parser_only

    with open(csv1, encoding="utf-8") as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
            parser.read_csv(m)
            assert not m.closed

