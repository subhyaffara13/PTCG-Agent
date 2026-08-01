
def test_scatter_logscale(fig_test, fig_ref):
    """
    Test scatter optimization with logarithmic scales.

    Ensures bounds checking works correctly in log-transformed coordinates.
    """
    rng = np.random.default_rng(19680801)

    # Create points across several orders of magnitude
    n_points = 50
    x = 10 ** (rng.random(n_points) * 4)  # 1 to 10000
    y = 10 ** (rng.random(n_points) * 4)
    c = rng.random(n_points)

    # Test figure: log scale with points mostly outside view
    ax_test = fig_test.subplots()
    ax_test.scatter(x, y, c=c, s=50)
    ax_test.set_xscale('log')
    ax_test.set_yscale('log')
    ax_test.set_xlim(100, 1000)  # Only show middle range
    ax_test.set_ylim(100, 1000)

    # Reference figure: should render identically
    ax_ref = fig_ref.subplots()
    ax_ref.scatter(x, y, c=c, s=50)
    ax_ref.set_xscale('log')
    ax_ref.set_yscale('log')
    ax_ref.set_xlim(100, 1000)
    ax_ref.set_ylim(100, 1000)

