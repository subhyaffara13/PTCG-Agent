
def test_invalid_file_buffer_mock(all_parsers):
    # see gh-15337
    parser = all_parsers
    msg = "Invalid file path or buffer object type"

    class Foo:
        pass

    with pytest.raises(ValueError, match=msg):
        parser.read_csv(Foo())

