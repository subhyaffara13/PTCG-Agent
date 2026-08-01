
def test_scatter3d_modification(fig_ref, fig_test):
    # Changing Path3DCollection properties post-creation should work correctly.
    ax_test = fig_test.add_subplot(projection='3d')
    c = ax_test.scatter(np.arange(10), np.arange(10), np.arange(10),
                        marker='o', depthshade=True)
    c.set_facecolor('C1')
    c.set_edgecolor('C2')
    c.set_alpha([0.3, 0.7] * 5)
    assert c.get_depthshade()
    c.set_depthshade(False)
    assert not c.get_depthshade()
    c.set_sizes(np.full(10, 75))
    c.set_linewidths(3)

    ax_ref = fig_ref.add_subplot(projection='3d')
    ax_ref.scatter(np.arange(10), np.arange(10), np.arange(10), marker='o',
                   facecolor='C1', edgecolor='C2', alpha=[0.3, 0.7] * 5,
                   depthshade=False, s=75, linewidths=3)

