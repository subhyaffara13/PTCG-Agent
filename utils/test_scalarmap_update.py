import itertools

def test_scalarmap_update(fig_test, fig_ref):

    x, y, z = np.array(list(itertools.product(*[np.arange(0, 5, 1),
                                                np.arange(0, 5, 1),
                                                np.arange(0, 5, 1)]))).T
    c = x + y

    # test
    ax_test = fig_test.add_subplot(111, projection='3d')
    sc_test = ax_test.scatter(x, y, z, c=c, s=40, cmap='viridis')
    # force a draw
    fig_test.canvas.draw()
    # mark it as "stale"
    sc_test.changed()

    # ref
    ax_ref = fig_ref.add_subplot(111, projection='3d')
    sc_ref = ax_ref.scatter(x, y, z, c=c, s=40, cmap='viridis')

