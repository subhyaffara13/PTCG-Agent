
def test_scatter3d_linewidth_modification(fig_ref, fig_test):
    # Changing Path3DCollection linewidths with array-like post-creation
    # should work correctly.
    ax_test = fig_test.add_subplot(projection='3d')
    c = ax_test.scatter(np.arange(10), np.arange(10), np.arange(10),
                        marker='o')
    c.set_linewidths(np.arange(10))

    ax_ref = fig_ref.add_subplot(projection='3d')
    ax_ref.scatter(np.arange(10), np.arange(10), np.arange(10), marker='o',
                   linewidths=np.arange(10))

