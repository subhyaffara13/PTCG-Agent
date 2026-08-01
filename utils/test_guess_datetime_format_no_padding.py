
def test_guess_datetime_format_no_padding(string, fmt, dayfirst, warning):
    # see gh-11142
    msg = (
        rf"Parsing dates in {fmt} format when dayfirst=False \(the default\) "
        "was specified. "
        "Pass `dayfirst=True` or specify a format to silence this warning."
    )
    with tm.assert_produces_warning(warning, match=msg):
        result = parsing.guess_datetime_format(string, dayfirst=dayfirst)
    assert result == fmt

