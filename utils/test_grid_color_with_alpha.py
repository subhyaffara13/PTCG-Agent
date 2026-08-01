
def test_grid_color_with_alpha():
    """Test that grid(color=(..., alpha)) respects the alpha value."""
    fig, ax = plt.subplots()
    ax.grid(True, color=(0.5, 0.6, 0.7, 0.3))

    # Check that alpha is extracted from color tuple
    for tick in ax.xaxis.get_major_ticks():
        assert tick.gridline.get_alpha() == 0.3, \
            f"Expected alpha=0.3, got {tick.gridline.get_alpha()}"

    for tick in ax.yaxis.get_major_ticks():
        assert tick.gridline.get_alpha() == 0.3, \
            f"Expected alpha=0.3, got {tick.gridline.get_alpha()}"

