
def test_uneven_length_cols(all_parsers, data, usecols, kwargs, expected):
    # see gh-8985
    parser = all_parsers
    result = parser.read_csv(StringIO(data), usecols=usecols, **kwargs)
    expected = DataFrame(expected)
    tm.assert_frame_equal(result, expected)

