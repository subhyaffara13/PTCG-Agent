
def test_ytickcolor_is_not_yticklabelcolor():
    plt.rcParams['ytick.color'] = 'yellow'
    plt.rcParams['ytick.labelcolor'] = 'blue'
    ax = plt.axes()
    ticks = ax.yaxis.get_major_ticks()
    for tick in ticks:
        assert tick.tick1line.get_color() == 'yellow'
        assert tick.label1.get_color() == 'blue'

