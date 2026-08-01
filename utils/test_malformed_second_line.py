
def test_malformed_second_line(all_parsers):
    # see GH14782
    parser = all_parsers
    data = "\na\nb\n"
    result = parser.read_csv(StringIO(data), skip_blank_lines=False, header=1)
    expected = DataFrame({"a": ["b"]})
    tm.assert_frame_equal(result, expected)

