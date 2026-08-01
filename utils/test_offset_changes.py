
def test_offset_changes():
    fig, ax = plt.subplots()

    d1 = datetime.datetime(1997, 1, 1)
    d2 = d1 + datetime.timedelta(weeks=520)

    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    ax.plot([d1, d2], [0, 0])
    fig.draw_without_rendering()
    assert formatter.get_offset() == ''
    ax.set_xlim(d1, d1 + datetime.timedelta(weeks=3))
    fig.draw_without_rendering()
    assert formatter.get_offset() == '1997-Jan'
    ax.set_xlim(d1 + datetime.timedelta(weeks=7),
                d1 + datetime.timedelta(weeks=30))
    fig.draw_without_rendering()
    assert formatter.get_offset() == '1997'
    ax.set_xlim(d1, d1 + datetime.timedelta(weeks=520))
    fig.draw_without_rendering()
    assert formatter.get_offset() == ''

