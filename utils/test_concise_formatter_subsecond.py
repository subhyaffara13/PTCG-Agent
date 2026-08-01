
def test_concise_formatter_subsecond():
    locator = mdates.AutoDateLocator(interval_multiples=True)
    formatter = mdates.ConciseDateFormatter(locator)
    year_1996 = 9861.0
    strings = formatter.format_ticks([
        year_1996,
        year_1996 + 500 / mdates.MUSECONDS_PER_DAY,
        year_1996 + 900 / mdates.MUSECONDS_PER_DAY])
    assert strings == ['00:00', '00.0005', '00.0009']

