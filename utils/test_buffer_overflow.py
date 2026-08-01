
def test_buffer_overflow(c_parser_only, malformed):
    # see gh-9205: test certain malformed input files that cause
    # buffer overflows in tokenizer.c
    msg = "Buffer overflow caught - possible malformed input file."
    parser = c_parser_only

    with pytest.raises(ParserError, match=msg):
        parser.read_csv(StringIO(malformed))

