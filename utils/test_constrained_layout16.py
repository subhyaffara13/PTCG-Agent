
def test_constrained_layout16():
    """Test ax.set_position."""
    fig, ax = plt.subplots(layout="constrained")
    example_plot(ax, fontsize=12)
    ax2 = fig.add_axes((0.2, 0.2, 0.4, 0.4))

