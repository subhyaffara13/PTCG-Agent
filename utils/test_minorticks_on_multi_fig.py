
def test_minorticks_on_multi_fig():
    """
    Turning on minor gridlines in a multi-Axes Figure
    that contains more than one boxplot and shares the x-axis
    should not raise an exception.
    """
    fig, ax = plt.subplots()

    ax.boxplot(np.arange(10), positions=[0])
    ax.boxplot(np.arange(10), positions=[0])
    ax.boxplot(np.arange(10), positions=[1])

    ax.grid(which="major")
    ax.grid(which="minor")
    ax.minorticks_on()
    fig.draw_without_rendering()

    assert ax.get_xgridlines()
    assert isinstance(ax.xaxis.get_minor_locator(), mpl.ticker.AutoMinorLocator)

