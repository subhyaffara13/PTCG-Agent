
def test_tight_layout1():
    """Test tight_layout for a single subplot."""
    fig, ax = plt.subplots()
    example_plot(ax, fontsize=24)
    plt.tight_layout()

