
def test_invalid_file_buffer_class(all_parsers):
    # see gh-15337
    class InvalidBuffer:
        pass

    parser = all_parsers
    msg = "Invalid file path or buffer object type"

    with pytest.raises(ValueError, match=msg):
        parser.read_csv(InvalidBuffer())

