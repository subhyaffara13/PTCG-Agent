
def test_cursor_data_nonuniform(xy, data):
    from matplotlib.backend_bases import MouseEvent

    # Non-linear set of x-values
    x = np.array([0, 1, 4, 9, 16])
    y = np.array([0, 1, 2, 3, 4])
    z = x[np.newaxis, :]**2 + y[:, np.newaxis]**2

    fig, ax = plt.subplots()
    im = NonUniformImage(ax, extent=(x.min(), x.max(), y.min(), y.max()))
    im.set_data(x, y, z)
    ax.add_image(im)
    # Set lower min lim so we can test cursor outside image
    ax.set_xlim(x.min() - 2, x.max())
    ax.set_ylim(y.min() - 2, y.max())

    xdisp, ydisp = ax.transData.transform(xy)
    event = MouseEvent('motion_notify_event', fig.canvas, xdisp, ydisp)
    assert im.get_cursor_data(event) == data, (im.get_cursor_data(event), data)

