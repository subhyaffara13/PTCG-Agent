
def test_internal_null_byte(c_parser_only):
    # see gh-14012
    #
    # The null byte ('\x00') should not be used as a
    # true line terminator, escape character, or comment
    # character, only as a placeholder to indicate that
    # none was specified.
    #
    # This test should be moved to test_common.py ONLY when
    # Python's csv class supports parsing '\x00'.
    parser = c_parser_only

    names = ["a", "b", "c"]
    data = "1,2,3\n4,\x00,6\n7,8,9"
    expected = DataFrame([[1, 2.0, 3], [4, np.nan, 6], [7, 8, 9]], columns=names)

    result = parser.read_csv(StringIO(data), names=names)
    tm.assert_frame_equal(result, expected)

