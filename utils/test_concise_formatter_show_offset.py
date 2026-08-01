
def test_concise_formatter_show_offset(t_delta, expected):
    d1 = datetime.datetime(1997, 1, 1)
    d2 = d1 + t_delta

    fig, ax = plt.subplots()
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    ax.plot([d1, d2], [0, 0])
    fig.canvas.draw()
    assert formatter.get_offset() == expected

