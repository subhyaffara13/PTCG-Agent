
def test_scale3d_all_clipped(fig_test, fig_ref):
    """Fully clipped data (e.g. negative values on log) should look like an empty plot.
    """
    lims = (0.1, 10)
    for ax in [fig_test.add_subplot(projection='3d'),
               fig_ref.add_subplot(projection='3d')]:
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_zscale('log')
        ax.set(xlim=lims, ylim=lims, zlim=lims)

    # All negative data — everything is invalid for log scale
    fig_test.axes[0].plot([-1, -2, -3], [-4, -5, -6], [-7, -8, -9])

