
def test_zoom_inset():
    dx, dy = 0.05, 0.05
    # generate 2 2d grids for the x & y bounds
    y, x = np.mgrid[slice(1, 5 + dy, dy),
                    slice(1, 5 + dx, dx)]
    z = np.sin(x)**10 + np.cos(10 + y*x) * np.cos(x)

    fig, ax = plt.subplots()
    ax.pcolormesh(x, y, z[:-1, :-1])
    ax.set_aspect(1.)
    ax.apply_aspect()
    # we need to apply_aspect to make the drawing below work.

    # Make the inset_axes...  Position axes coordinates...
    axin1 = ax.inset_axes([0.7, 0.7, 0.35, 0.35])
    # redraw the data in the inset axes...
    axin1.pcolormesh(x, y, z[:-1, :-1])
    axin1.set_xlim(1.5, 2.15)
    axin1.set_ylim(2, 2.5)
    axin1.set_aspect(ax.get_aspect())

    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        rec, connectors = ax.indicate_inset_zoom(axin1)
    fig.canvas.draw()
    assert len(connectors) == 4
    xx = np.array([[1.5,  2.],
                   [2.15, 2.5]])
    assert np.all(rec.get_bbox().get_points() == xx)
    xx = np.array([[0.6325, 0.692308],
                   [0.8425, 0.907692]])
    np.testing.assert_allclose(
        axin1.get_position().get_points(), xx, rtol=1e-4)

