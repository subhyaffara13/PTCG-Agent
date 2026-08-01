
def test_plot_scatter_masks(fig_test, fig_ref):
    x = np.linspace(0, 10, 100)
    y = np.linspace(0, 10, 100)
    z = np.sin(x) * np.cos(y)
    mask = z > 0

    z_masked = np.ma.array(z, mask=mask)
    ax_test = fig_test.add_subplot(projection='3d')
    ax_test.scatter(x, y, z_masked)
    ax_test.plot(x, y, z_masked)

    x[mask] = y[mask] = z[mask] = np.nan
    ax_ref = fig_ref.add_subplot(projection='3d')
    ax_ref.scatter(x, y, z)
    ax_ref.plot(x, y, z)

