
def test_tight_layout8():
    """Test automatic use of tight_layout."""
    fig = plt.figure()
    fig.set_layout_engine(layout='tight', pad=0.1)
    ax = fig.add_subplot()
    example_plot(ax, fontsize=24)
    fig.draw_without_rendering()

