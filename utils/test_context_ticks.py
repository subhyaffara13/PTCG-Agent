
def test_context_ticks():
    with plt.rc_context({
            'xtick.direction': 'in', 'xtick.major.size': 30, 'xtick.major.width': 5,
            'xtick.color': 'C0', 'xtick.major.pad': 12,
            'xtick.bottom': True, 'xtick.top': True,
            'xtick.labelsize': 14, 'xtick.labelcolor': 'C1'}):
        fig, ax = plt.subplots()
    # Draw outside the context so that all-but-first tick are generated with the normal
    # mpl20 style in place.
    fig.draw_without_rendering()

    first_tick = ax.xaxis.majorTicks[0]
    for tick in ax.xaxis.majorTicks[1:]:
        assert tick._size == first_tick._size
        assert tick._width == first_tick._width
        assert tick._base_pad == first_tick._base_pad
        assert tick._labelrotation == first_tick._labelrotation
        assert tick._zorder == first_tick._zorder
        assert tick._tickdir == first_tick._tickdir

