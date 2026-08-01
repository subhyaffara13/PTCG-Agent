
def test_format_coord():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    x = np.arange(10)
    ax.plot(x, np.sin(x))
    xv = 0.1
    yv = 0.1
    fig.canvas.draw()
    assert ax.format_coord(xv, yv) == 'x=10.5227, y pane=1.0417, z=0.1444'

    # Modify parameters
    ax.view_init(roll=30, vertical_axis="y")
    fig.canvas.draw()
    assert ax.format_coord(xv, yv) == 'x pane=9.1875, y=0.9761, z=0.1291'

    # Reset parameters
    ax.view_init()
    fig.canvas.draw()
    assert ax.format_coord(xv, yv) == 'x=10.5227, y pane=1.0417, z=0.1444'

    # Check orthographic projection
    ax.set_proj_type('ortho')
    fig.canvas.draw()
    assert ax.format_coord(xv, yv) == 'x=10.8869, y pane=1.0417, z=0.1528'

    # Check non-default perspective projection
    ax.set_proj_type('persp', focal_length=0.1)
    fig.canvas.draw()
    assert ax.format_coord(xv, yv) == 'x=9.0620, y pane=1.0417, z=0.1110'

