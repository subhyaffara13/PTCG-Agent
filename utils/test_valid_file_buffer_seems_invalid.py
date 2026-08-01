
def test_valid_file_buffer_seems_invalid(all_parsers):
    # gh-16135: we want to ensure that "tell" and "seek"
    # aren't actually being used when we call `read_csv`
    #
    # Thus, while the object may look "invalid" (these
    # methods are attributes of the `StringIO` class),
    # it is still a valid file-object for our purposes.
    class NoSeekTellBuffer(StringIO):
        def tell(self):
            raise AttributeError("No tell method")

        def seek(self, pos, whence=0):
            raise AttributeError("No seek method")

    data = "a\n1"
    parser = all_parsers
    expected = DataFrame({"a": [1]})

    result = parser.read_csv(NoSeekTellBuffer(data))
    tm.assert_frame_equal(result, expected)

