
def test_chunk_whitespace_on_boundary(c_parser_only):
    # see gh-9735: this issue is C parser-specific (bug when
    # parsing whitespace and characters at chunk boundary)
    #
    # This test case has a field too large for the Python parser / CSV library.
    parser = c_parser_only

    chunk1 = "a" * (1024 * 256 - 2) + "\na"
    chunk2 = "\n a"
    result = parser.read_csv(StringIO(chunk1 + chunk2), header=None)

    expected = DataFrame(["a" * (1024 * 256 - 2), "a", " a"])
    tm.assert_frame_equal(result, expected)

