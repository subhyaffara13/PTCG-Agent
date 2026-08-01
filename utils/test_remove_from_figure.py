
def test_remove_from_figure(nested_gridspecs, use_gridspec):
    """Test `remove` with the specified ``use_gridspec`` setting."""
    fig = plt.figure()
    if nested_gridspecs:
        gs = fig.add_gridspec(2, 2)[1, 1].subgridspec(2, 2)
        ax = fig.add_subplot(gs[1, 1])
    else:
        ax = fig.add_subplot()
    sc = ax.scatter([1, 2], [3, 4])
    sc.set_array(np.array([5, 6]))
    pre_position = ax.get_position()
    cb = fig.colorbar(sc, use_gridspec=use_gridspec)
    fig.subplots_adjust()
    cb.remove()
    fig.subplots_adjust()
    post_position = ax.get_position()
    assert (pre_position.get_points() == post_position.get_points()).all()

