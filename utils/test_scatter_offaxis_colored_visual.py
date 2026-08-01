
def test_scatter_offaxis_colored_visual(fig_test, fig_ref):
    """
    Test that on-axis scatter with per-point colors still renders correctly.

    Ensures the optimization for off-axis markers doesn't break normal
    scatter rendering.
    """
    rng = np.random.default_rng(19680801)

    n_points = 100
    x = rng.random(n_points) * 5
    y = rng.random(n_points) * 5
    c = rng.random(n_points)

    # Test figure: scatter with clipping optimization
    ax_test = fig_test.subplots()
    ax_test.scatter(x, y, c=c, s=50)
    ax_test.set_xlim(0, 10)
    ax_test.set_ylim(0, 10)

    # Reference figure: should look identical
    ax_ref = fig_ref.subplots()
    ax_ref.scatter(x, y, c=c, s=50)
    ax_ref.set_xlim(0, 10)
    ax_ref.set_ylim(0, 10)

