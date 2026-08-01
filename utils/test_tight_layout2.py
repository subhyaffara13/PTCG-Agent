
def test_tight_layout2():
    """Test tight_layout for multiple subplots."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
    example_plot(ax1)
    example_plot(ax2)
    example_plot(ax3)
    example_plot(ax4)
    plt.tight_layout()

