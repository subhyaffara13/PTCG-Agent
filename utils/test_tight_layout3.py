
def test_tight_layout3():
    """Test tight_layout for multiple subplots."""
    ax1 = plt.subplot(221)
    ax2 = plt.subplot(223)
    ax3 = plt.subplot(122)
    example_plot(ax1)
    example_plot(ax2)
    example_plot(ax3)
    plt.tight_layout()

