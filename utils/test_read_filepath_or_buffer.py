
def test_read_filepath_or_buffer(all_parsers):
    # see gh-43366
    parser = all_parsers

    with pytest.raises(TypeError, match="Expected file path name or file-like"):
        parser.read_csv(filepath_or_buffer=b"input")

