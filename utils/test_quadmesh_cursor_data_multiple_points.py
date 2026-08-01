
def test_quadmesh_cursor_data_multiple_points():
    x = [1, 2, 1, 2]
    fig, ax = plt.subplots()
    mesh = ax.pcolormesh(x, x, np.ones((3, 3)))
    fig.draw_without_rendering()
    xdata, ydata = 1.5, 1.5
    x, y = mesh.get_transform().transform((xdata, ydata))
    mouse_event = SimpleNamespace(xdata=xdata, ydata=ydata, x=x, y=y)
    # All quads are covering the same square
    assert_array_equal(mesh.get_cursor_data(mouse_event), np.ones(9))

