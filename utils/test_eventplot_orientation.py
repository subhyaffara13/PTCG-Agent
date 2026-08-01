
def test_eventplot_orientation(data, orientation):
    """Introduced when fixing issue #6412."""
    opts = {} if orientation is None else {'orientation': orientation}
    fig, ax = plt.subplots(1, 1)
    ax.eventplot(data, **opts)
    plt.draw()

