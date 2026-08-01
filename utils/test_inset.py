
def test_inset():
    """
    Ensure that inset_ax argument is indeed optional
    """
    dx, dy = 0.05, 0.05
    # generate 2 2d grids for the x & y bounds
    y, x = np.mgrid[slice(1, 5 + dy, dy),
                    slice(1, 5 + dx, dx)]
    z = np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

    fig, ax = plt.subplots()
    ax.pcolormesh(x, y, z[:-1, :-1])
    ax.set_aspect(1.)
    ax.apply_aspect()
    # we need to apply_aspect to make the drawing below work.

    xlim = [1.5, 2.15]
    ylim = [2, 2.5]

    rect = [xlim[0], ylim[0], xlim[1] - xlim[0], ylim[1] - ylim[0]]

    inset = ax.indicate_inset(bounds=rect)
    assert inset.connectors is None
    fig.canvas.draw()
    xx = np.array([[1.5, 2.],
                   [2.15, 2.5]])
    assert np.all(inset.rectangle.get_bbox().get_points() == xx)

