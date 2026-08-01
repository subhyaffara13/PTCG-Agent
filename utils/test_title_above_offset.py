
def test_title_above_offset(left, center):
    # Test that title moves if overlaps with yaxis offset text.
    mpl.rcParams['axes.titley'] = None
    fig, ax = plt.subplots()
    ax.set_ylim(1e11)
    ax.set_title(left, loc='left')
    ax.set_title(center)
    fig.draw_without_rendering()
    if left and not center:
        assert ax._left_title.get_position()[1] > 1.0
    elif not left and center:
        assert ax.title.get_position()[1] == 1.0
    else:
        yleft = ax._left_title.get_position()[1]
        ycenter = ax.title.get_position()[1]
        assert yleft > 1.0
        assert ycenter == yleft

