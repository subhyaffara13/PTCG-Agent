
def test_concise_formatter_usetex(t_delta, expected):
    d1 = datetime.datetime(1997, 1, 1)
    d2 = d1 + t_delta

    locator = mdates.AutoDateLocator(interval_multiples=True)
    locator.create_dummy_axis()
    locator.axis.set_view_interval(mdates.date2num(d1), mdates.date2num(d2))

    formatter = mdates.ConciseDateFormatter(locator, usetex=True)
    assert formatter.format_ticks(locator()) == expected

