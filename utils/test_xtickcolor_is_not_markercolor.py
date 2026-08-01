
def test_xtickcolor_is_not_markercolor():
    plt.rcParams['lines.markeredgecolor'] = 'white'
    ax = plt.axes()
    ticks = ax.xaxis.get_major_ticks()
    for tick in ticks:
        assert tick.tick1line.get_markeredgecolor() != 'white'

