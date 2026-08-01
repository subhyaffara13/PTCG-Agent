
def test_grow_boundary_at_cap(c_parser_only, count):
    # See gh-12494
    #
    # Cause of error was that the C parser
    # was not increasing the buffer size when
    # the desired space would fill the buffer
    # to capacity, which would later cause a
    # buffer overflow error when checking the
    # EOF terminator of the CSV stream.
    # 3 * 2^n commas was observed to break the parser
    parser = c_parser_only

    with StringIO("," * count) as s:
        expected = DataFrame(columns=[f"Unnamed: {i}" for i in range(count + 1)])
        df = parser.read_csv(s)
    tm.assert_frame_equal(df, expected)

