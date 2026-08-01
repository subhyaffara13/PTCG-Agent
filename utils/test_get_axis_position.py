
def test_get_axis_position():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    x = np.arange(10)
    ax.plot(x, np.sin(x))
    fig.canvas.draw()
    assert ax.get_axis_position() == (False, True, False)

