
def test_scale3d_default_limits(scale, expected_lims):
    """Default axis limits on an empty plot should be correct for each scale."""
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_xscale(scale)
    ax.set_yscale(scale)
    ax.set_zscale(scale)
    fig.canvas.draw()

    for get_lim in (ax.get_xlim, ax.get_ylim, ax.get_zlim):
        np.testing.assert_allclose(get_lim(), expected_lims)

