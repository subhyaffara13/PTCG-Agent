
def test_suppress_error_output(all_parsers):
    # see gh-15925
    parser = all_parsers
    data = "a\n1\n1,2,3\n4\n5,6,7"
    expected = DataFrame({"a": [1, 4]})

    result = parser.read_csv(StringIO(data), on_bad_lines="skip")
    tm.assert_frame_equal(result, expected)

