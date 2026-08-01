
def test_guess_datetime_format_with_dayfirst(dayfirst, expected):
    ambiguous_string = "01/01/2011"
    result = parsing.guess_datetime_format(ambiguous_string, dayfirst=dayfirst)
    assert result == expected

