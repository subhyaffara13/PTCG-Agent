
def test_raises_on_usecols_names_mismatch(
    all_parsers, usecols, kwargs, expected, msg, request
):
    data = "a,b,c,d\n1,2,3,4\n5,6,7,8"
    kwargs.update(usecols=usecols)
    parser = all_parsers

    if parser.engine == "pyarrow" and not (
        usecols is not None and expected is not None
    ):
        # everything but the first case
        # ArrowKeyError: Column 'f' in include_columns does not exist in CSV file
        pytest.skip(reason="https://github.com/apache/arrow/issues/38676")

    if expected is None:
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), **kwargs)
    else:
        result = parser.read_csv(StringIO(data), **kwargs)
        tm.assert_frame_equal(result, expected)

