
def test_quadmesh_contains():
    x = np.arange(4)
    X = x[:, None] * x[None, :]

    fig, ax = plt.subplots()
    mesh = ax.pcolormesh(X)
    fig.draw_without_rendering()
    xdata, ydata = 0.5, 0.5
    x, y = mesh.get_transform().transform((xdata, ydata))
    mouse_event = SimpleNamespace(xdata=xdata, ydata=ydata, x=x, y=y)
    found, indices = mesh.contains(mouse_event)
    assert found
    assert_array_equal(indices['ind'], [0])

    xdata, ydata = 1.5, 1.5
    x, y = mesh.get_transform().transform((xdata, ydata))
    mouse_event = SimpleNamespace(xdata=xdata, ydata=ydata, x=x, y=y)
    found, indices = mesh.contains(mouse_event)
    assert found
    assert_array_equal(indices['ind'], [5])

