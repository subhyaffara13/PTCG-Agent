
def test_constrained_layout17():
    """Test uneven gridspecs"""
    fig = plt.figure(layout="constrained")
    gs = gridspec.GridSpec(3, 3, figure=fig)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1:])
    ax3 = fig.add_subplot(gs[1:, 0:2])
    ax4 = fig.add_subplot(gs[1:, -1])

    example_plot(ax1)
    example_plot(ax2)
    example_plot(ax3)
    example_plot(ax4)

