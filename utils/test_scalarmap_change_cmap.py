import itertools

def test_scalarmap_change_cmap(fig_test, fig_ref):
    # Ensure that changing the colormap of a 3D scatter after draw updates the colors.

    x, y, z = np.array(list(itertools.product(
        np.arange(0, 5, 1),
        np.arange(0, 5, 1),
        np.arange(0, 5, 1)
    ))).T
    c = x + y

    # test
    ax_test = fig_test.add_subplot(111, projection='3d')
    sc_test = ax_test.scatter(x, y, z, c=c, s=40, cmap='jet')
    fig_test.canvas.draw()
    sc_test.set_cmap('viridis')

    # ref
    ax_ref = fig_ref.add_subplot(111, projection='3d')
    ax_ref.scatter(x, y, z, c=c, s=40, cmap='viridis')

