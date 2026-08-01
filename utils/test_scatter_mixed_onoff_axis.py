
def test_scatter_mixed_onoff_axis(fig_test, fig_ref):
    """
    Test scatter with some points on-axis and some off-axis.

    Ensures the optimization correctly handles the common case where only
    some markers are outside the visible area.
    """
    rng = np.random.default_rng(19680801)

    # Create points: half on-axis (0-5), half off-axis (15-20)
    n_points = 50
    x_on = rng.random(n_points) * 5
    y_on = rng.random(n_points) * 5
    x_off = rng.random(n_points) * 5 + 15
    y_off = rng.random(n_points) * 5 + 15

    x = np.concatenate([x_on, x_off])
    y = np.concatenate([y_on, y_off])
    c = rng.random(2 * n_points)

    # Test figure: scatter with mixed points
    ax_test = fig_test.subplots()
    ax_test.scatter(x, y, c=c, s=50)
    ax_test.set_xlim(0, 10)
    ax_test.set_ylim(0, 10)

    # Reference figure: only the on-axis points should be visible
    ax_ref = fig_ref.subplots()
    ax_ref.scatter(x_on, y_on, c=c[:n_points], s=50)
    ax_ref.set_xlim(0, 10)
    ax_ref.set_ylim(0, 10)

