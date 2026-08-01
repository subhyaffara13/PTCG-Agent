
def test_skip_row_with_newline(all_parsers, data, kwargs, expected):
    # see gh-12775 and gh-10911
    parser = all_parsers
    result = parser.read_csv(StringIO(data), **kwargs)
    tm.assert_frame_equal(result, expected)

