
def test_remove_from_figure_cl():
    """Test `remove` with constrained_layout."""
    fig, ax = plt.subplots(constrained_layout=True)
    sc = ax.scatter([1, 2], [3, 4])
    sc.set_array(np.array([5, 6]))
    fig.draw_without_rendering()
    pre_position = ax.get_position()
    cb = fig.colorbar(sc)
    cb.remove()
    fig.draw_without_rendering()
    post_position = ax.get_position()
    np.testing.assert_allclose(pre_position.get_points(),
                               post_position.get_points())

