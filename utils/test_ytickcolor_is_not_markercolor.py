
def test_ytickcolor_is_not_markercolor():
    plt.rcParams['lines.markeredgecolor'] = 'white'
    ax = plt.axes()
    ticks = ax.yaxis.get_major_ticks()
    for tick in ticks:
        assert tick.tick1line.get_markeredgecolor() != 'white'

