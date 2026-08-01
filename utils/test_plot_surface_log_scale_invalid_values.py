
def test_plot_surface_log_scale_invalid_values():
    """Ensure non-positive Z values on a log z-axis does not corrupt zlim."""
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_zscale('log')
    X, Y = np.meshgrid(np.linspace(1, 3, 4), np.linspace(1, 3, 4))
    Z = X * Y - 4  # half the entries are <= 0, invalid for a log scale
    ax.plot_surface(X, Y, Z)
    fig.canvas.draw()

    zmin, zmax = ax.get_zlim()
    assert 1e-3 < zmin < zmax < 1e3, f"zlim corrupted: {(zmin, zmax)}"

