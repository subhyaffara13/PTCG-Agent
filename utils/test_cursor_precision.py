
def test_cursor_precision():
    ax = plt.subplot(projection="polar")
    # Higher radii correspond to higher theta-precisions.
    assert ax.format_coord(0, 0.005) == "θ=0.0π (0°), r=0.005"
    assert ax.format_coord(0, .1) == "θ=0.00π (0°), r=0.100"
    assert ax.format_coord(0, 1) == "θ=0.000π (0.0°), r=1.000"
    assert ax.format_coord(1, 0.005) == "θ=0.3π (57°), r=0.005"
    assert ax.format_coord(1, .1) == "θ=0.32π (57°), r=0.100"
    assert ax.format_coord(1, 1) == "θ=0.318π (57.3°), r=1.000"
    assert ax.format_coord(2, 0.005) == "θ=0.6π (115°), r=0.005"
    assert ax.format_coord(2, .1) == "θ=0.64π (115°), r=0.100"
    assert ax.format_coord(2, 1) == "θ=0.637π (114.6°), r=1.000"

