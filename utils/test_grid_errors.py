
def test_grid_errors(rect, n_axes, error, message):
    fig = plt.figure()
    with pytest.raises(error, match=message):
        Grid(fig, rect, (2, 3), n_axes=n_axes)

