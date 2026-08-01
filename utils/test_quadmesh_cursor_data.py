
def test_quadmesh_cursor_data():
    x = np.arange(4)
    X = x[:, None] * x[None, :]

    fig, ax = plt.subplots()
    mesh = ax.pcolormesh(X)
    # Empty array data
    mesh._A = None
    fig.draw_without_rendering()
    xdata, ydata = 0.5, 0.5
    x, y = mesh.get_transform().transform((xdata, ydata))
    mouse_event = SimpleNamespace(xdata=xdata, ydata=ydata, x=x, y=y)
    # Empty collection should return None
    assert mesh.get_cursor_data(mouse_event) is None

    # Now test adding the array data, to make sure we do get a value
    mesh.set_array(np.ones(X.shape))
    assert_array_equal(mesh.get_cursor_data(mouse_event), [1])

