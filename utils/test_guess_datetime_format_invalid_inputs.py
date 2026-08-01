
def test_guess_datetime_format_invalid_inputs(invalid_dt):
    # A datetime string must include a year, month and a day for it to be
    # guessable, in addition to being a string that looks like a datetime.
    assert parsing.guess_datetime_format(invalid_dt) is None

