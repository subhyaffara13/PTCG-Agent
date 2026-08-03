import re

def test_guess_datetime_format_with_parseable_formats(string, fmt):
    with tm.maybe_produces_warning(
        UserWarning, fmt is not None and re.search(r"%d.*%m", fmt)
    ):
        result = parsing.guess_datetime_format(string)
    assert result == fmt

