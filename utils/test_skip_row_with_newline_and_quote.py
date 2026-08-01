
def test_skip_row_with_newline_and_quote(all_parsers, data, exp_data):
    # see gh-12775 and gh-10911
    parser = all_parsers
    result = parser.read_csv(StringIO(data), skiprows=[1])

    expected = DataFrame(exp_data, columns=["id", "text", "num_lines"])
    tm.assert_frame_equal(result, expected)

