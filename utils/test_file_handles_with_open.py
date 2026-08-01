
def test_file_handles_with_open(all_parsers, csv1):
    # gh-14418
    #
    # Don't close user provided file handles.
    parser = all_parsers

    for mode in ["r", "rb"]:
        with open(csv1, mode, encoding="utf-8" if mode == "r" else None) as f:
            parser.read_csv(f)
            assert not f.closed

