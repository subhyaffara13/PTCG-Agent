
def test_numeric_positions_with_float_widths_ok():
    """Test that numeric positions with float widths work."""
    fig, ax = plt.subplots()
    positions = [1.0, 2.0]
    widths = [0.5, 1.0]
    ax.violin(violin_plot_stats(), positions=positions, widths=widths)

