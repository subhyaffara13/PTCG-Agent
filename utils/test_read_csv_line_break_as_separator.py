
def test_read_csv_line_break_as_separator(kwargs, all_parsers):
    # GH#43528
    parser = all_parsers
    data = """a,b,c
1,2,3
    """
    msg = (
        r"Specified \\n as separator or delimiter. This forces the python engine "
        r"which does not accept a line terminator. Hence it is not allowed to use "
        r"the line terminator as separator."
    )
    with pytest.raises(ValueError, match=msg):
        parser.read_csv(StringIO(data), **kwargs)

