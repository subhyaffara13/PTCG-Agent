
def test_guess_datetime_format_with_locale_specific_formats(string, fmt):
    result = parsing.guess_datetime_format(string)
    assert result == fmt

