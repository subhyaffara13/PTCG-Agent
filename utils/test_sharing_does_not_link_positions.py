
def test_sharing_does_not_link_positions():
    fig = plt.figure()
    ax0 = fig.add_subplot(221)
    ax1 = fig.add_axes((.6, .6, .3, .3), sharex=ax0)
    init_pos = ax1.get_position()
    fig.subplots_adjust(left=0)
    assert (ax1.get_position().get_points() == init_pos.get_points()).all()

