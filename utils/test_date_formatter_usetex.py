
def test_date_formatter_usetex(delta, expected):
    style.use("default")

    d1 = datetime.datetime(1990, 1, 1)
    d2 = d1 + delta

    locator = mdates.AutoDateLocator(interval_multiples=False)
    locator.create_dummy_axis()
    locator.axis.set_view_interval(mdates.date2num(d1), mdates.date2num(d2))

    formatter = mdates.AutoDateFormatter(locator, usetex=True)
    assert [formatter(loc) for loc in locator()] == expected

