
def test_scatter3d_cmap_alpha(fig_ref, fig_test):
    # Check that alpha is applied correctly with colormapped scatter.
    # Regression test for https://github.com/matplotlib/matplotlib/issues/25468
    x, y, z = np.arange(5), np.zeros(5), np.arange(5)
    c = np.array([0, 1, np.nan, 3, 4])

    ax_test = fig_test.add_subplot(projection='3d')
    ax_test.scatter(x, y, z, c=c)
    ax_ref = fig_ref.add_subplot(projection='3d')
    ax_ref.scatter(x, y, z, c=c, alpha=1)

