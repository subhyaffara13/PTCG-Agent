
def test_norm_update_figs(fig_test, fig_ref):
    ax_ref = fig_ref.add_subplot()
    ax_test = fig_test.add_subplot()

    z = np.arange(100).reshape((10, 10))
    ax_ref.imshow(z, norm=mcolors.Normalize(10, 90))

    # Create the norm beforehand with different limits and then update
    # after adding to the plot
    norm = mcolors.Normalize(0, 1)
    ax_test.imshow(z, norm=norm)
    # Force initial draw to make sure it isn't already stale
    fig_test.canvas.draw()
    norm.vmin, norm.vmax = 10, 90

