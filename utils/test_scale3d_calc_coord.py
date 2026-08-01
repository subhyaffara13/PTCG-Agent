
def test_scale3d_calc_coord():
    """_calc_coord should return data coordinates with correct pane values."""
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter([1, 10, 100], [1, 10, 100], [1, 10, 100])
    ax.set(xscale='log', yscale='log', zscale='log')
    fig.canvas.draw()

    point, pane_idx = ax._calc_coord(0.5, 0.5)
    # Pane coordinate should match axis limit (y-pane at max)
    assert pane_idx == 1
    assert point[pane_idx] == pytest.approx(ax.get_ylim()[1])

