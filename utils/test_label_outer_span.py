
def test_label_outer_span():
    fig = plt.figure()
    gs = fig.add_gridspec(3, 3)
    # +---+---+---+
    # |   1   |   |
    # +---+---+---+
    # |   |   | 3 |
    # + 2 +---+---+
    # |   | 4 |   |
    # +---+---+---+
    a1 = fig.add_subplot(gs[0, 0:2])
    a2 = fig.add_subplot(gs[1:3, 0])
    a3 = fig.add_subplot(gs[1, 2])
    a4 = fig.add_subplot(gs[2, 1])
    for ax in fig.axes:
        ax.label_outer()
    check_ticklabel_visible(
        fig.axes, [False, True, False, True], [True, True, False, False])

