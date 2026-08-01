
def test_widgetlock_zoompan():
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    fig.canvas.widgetlock(ax)
    tb = NavigationToolbar2(fig.canvas)
    tb.zoom()
    assert ax.get_navigate_mode() is None
    tb.pan()
    assert ax.get_navigate_mode() is None

