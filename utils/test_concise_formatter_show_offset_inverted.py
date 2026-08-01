
def test_concise_formatter_show_offset_inverted():
    # Test for github issue #28481
    d1 = datetime.datetime(1997, 1, 1)
    d2 = d1 + datetime.timedelta(days=60)

    fig, ax = plt.subplots()
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.invert_xaxis()

    ax.plot([d1, d2], [0, 0])
    fig.canvas.draw()
    assert formatter.get_offset() == '1997-Jan'

