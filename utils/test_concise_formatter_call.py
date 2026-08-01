
def test_concise_formatter_call():
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    assert formatter(19002.0) == '2022'
    assert formatter.format_data_short(19002.0) == '2022-01-10 00:00:00'

