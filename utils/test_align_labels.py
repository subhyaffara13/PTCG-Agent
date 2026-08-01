
def test_align_labels():
    """
    Tests for a bug in which constrained layout and align_ylabels on
    three unevenly sized subplots, one of whose y tick labels include
    negative numbers, drives the non-negative subplots' y labels off
    the edge of the plot
    """
    fig, (ax3, ax1, ax2) = plt.subplots(3, 1, layout="constrained",
                                        figsize=(6.4, 8),
                                        gridspec_kw={"height_ratios": (1, 1,
                                                                       0.7)})

    ax1.set_ylim(0, 1)
    ax1.set_ylabel("Label")

    ax2.set_ylim(-1.5, 1.5)
    ax2.set_ylabel("Label")

    ax3.set_ylim(0, 1)
    ax3.set_ylabel("Label")

    fig.align_ylabels(axs=(ax3, ax1, ax2))

    fig.draw_without_rendering()
    after_align = [ax1.yaxis.label.get_window_extent(),
                   ax2.yaxis.label.get_window_extent(),
                   ax3.yaxis.label.get_window_extent()]
    # ensure labels are approximately aligned
    np.testing.assert_allclose([after_align[0].x0, after_align[2].x0],
                               after_align[1].x0, rtol=0, atol=1e-05)
    # ensure labels do not go off the edge
    assert after_align[0].x0 >= 1


def test_align_labels():
    fig = plt.figure(layout='tight')
    gs = gridspec.GridSpec(3, 3)

    ax = fig.add_subplot(gs[0, :2])
    ax.plot(np.arange(0, 1e6, 1000))
    ax.set_ylabel('Ylabel0 0')
    ax = fig.add_subplot(gs[0, -1])
    ax.plot(np.arange(0, 1e4, 100))

    for i in range(3):
        ax = fig.add_subplot(gs[1, i])
        ax.set_ylabel('YLabel1 %d' % i)
        ax.set_xlabel('XLabel1 %d' % i)
        if i in [0, 2]:
            ax.xaxis.set_label_position("top")
            ax.xaxis.tick_top()
        if i == 0:
            for tick in ax.get_xticklabels():
                tick.set_rotation(90)
        if i == 2:
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()

    for i in range(3):
        ax = fig.add_subplot(gs[2, i])
        ax.set_xlabel(f'XLabel2 {i}')
        ax.set_ylabel(f'YLabel2 {i}')

        if i == 2:
            ax.plot(np.arange(0, 1e4, 10))
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
            for tick in ax.get_xticklabels():
                tick.set_rotation(90)

    fig.align_labels()

