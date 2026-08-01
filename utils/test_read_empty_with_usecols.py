
def test_read_empty_with_usecols(all_parsers, data, kwargs, expected):
    # see gh-12493
    parser = all_parsers

    if expected is None:
        msg = "No columns to parse from file"
        with pytest.raises(EmptyDataError, match=msg):
            parser.read_csv(StringIO(data), **kwargs)
    else:
        result = parser.read_csv(StringIO(data), **kwargs)
        tm.assert_frame_equal(result, expected)

