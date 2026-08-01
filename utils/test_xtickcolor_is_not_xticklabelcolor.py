
def test_xtickcolor_is_not_xticklabelcolor():
    plt.rcParams['xtick.color'] = 'yellow'
    plt.rcParams['xtick.labelcolor'] = 'blue'
    ax = plt.axes()
    ticks = ax.xaxis.get_major_ticks()
    for tick in ticks:
        assert tick.tick1line.get_color() == 'yellow'
        assert tick.label1.get_color() == 'blue'

