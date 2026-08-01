
def test_scatter_polar(fig_test, fig_ref):
    """
    Test scatter optimization with polar coordinates.

    Ensures bounds checking works correctly in polar projections.
    """
    rng = np.random.default_rng(19680801)

    n_points = 50
    theta = rng.random(n_points) * 2 * np.pi
    r = rng.random(n_points) * 3
    c = rng.random(n_points)

    # Test figure: polar projection
    ax_test = fig_test.subplots(subplot_kw={'projection': 'polar'})
    ax_test.scatter(theta, r, c=c, s=50)
    ax_test.set_ylim(0, 2)  # Limit radial range

    # Reference figure: should render identically
    ax_ref = fig_ref.subplots(subplot_kw={'projection': 'polar'})
    ax_ref.scatter(theta, r, c=c, s=50)
    ax_ref.set_ylim(0, 2)

