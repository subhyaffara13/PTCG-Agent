
def test_quadmesh_contains_concave():
    # Test a concave polygon, V-like shape
    x = [[0, -1], [1, 0]]
    y = [[0, 1], [1, -1]]
    fig, ax = plt.subplots()
    mesh = ax.pcolormesh(x, y, [[0]])
    fig.draw_without_rendering()
    # xdata, ydata, expected
    points = [(-0.5, 0.25, True),  # left wing
              (0, 0.25, False),  # between the two wings
              (0.5, 0.25, True),  # right wing
              (0, -0.25, True),  # main body
              ]
    for point in points:
        xdata, ydata, expected = point
        x, y = mesh.get_transform().transform((xdata, ydata))
        mouse_event = SimpleNamespace(xdata=xdata, ydata=ydata, x=x, y=y)
        found, indices = mesh.contains(mouse_event)
        assert found is expected

